"""
LangGraph orchestration - Router + Sub-agents with RAG retrieval and tool calling.
"""
import logging
from typing import AsyncIterator, Literal, TypedDict

from app.llm.provider import get_llm
from app.orchestrator.prompts import get_system_prompt
from app.tools import get_tools_for_agent

logger = logging.getLogger(__name__)

MAX_ITERATIONS = 8


# Define the state for our graph
class AgentState(TypedDict):
    messages: list[dict]
    assistant_id: str
    mode: str
    context: dict
    response_chunks: list[str]


# Router: determine which agent to use based on assistant_id
def get_agent_name(assistant_id: str) -> str:
    """Map assistant_id to agent name."""
    mapping = {
        "tasks": "task",
        "task": "task",
        "project": "project",
        "coach": "coach",
        "files": "file",
        "file": "file",
        "chat": "chat",
        "workspace": "chat",
    }
    return mapping.get(assistant_id, "chat")


def _extract_query(messages: list[dict]) -> str:
    """Extract the last user message as the query."""
    for msg in reversed(messages):
        if msg.get("role") == "user" and msg.get("content"):
            return msg["content"]
    return ""


async def _retrieve_context(query: str, assistant_id: str) -> str:
    """Retrieve relevant documents using RAG."""
    try:
        from app.rag.retriever import get_retriever
        retriever = get_retriever()
        result = await retriever.retrieve(query, top_k=3)
        return result.context_text
    except Exception as e:
        logger.warning("rag_retrieve_failed", extra={"query": query, "error": str(e)})
        return ""


def _parse_tool_calls(llm_response: str) -> list[dict] | None:
    """Extract tool calls from LLM response (simplified parsing)."""
    import json
    import re
    # Look for JSON blocks containing tool_calls
    match = re.search(r'\{[^{}]*"tool_calls"[^{}]*\}', llm_response, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return data.get("tool_calls")
        except json.JSONDecodeError:
            pass
    return None


async def _execute_tools(tool_calls: list[dict], agent_name: str) -> list[dict]:
    """Execute tool calls and return results as messages."""
    registry = get_tools_for_agent(agent_name)
    if not registry:
        return [{"role": "system", "content": "工具不可用"}]

    results = []
    for tc in tool_calls:
        name = tc.get("name", "")
        args = tc.get("arguments", {})
        try:
            # Write tools require actionCard confirmation - skip direct execution
            if registry.is_write_tool(name):
                results.append({
                    "role": "tool",
                    "content": f"工具 {name} 需要用户确认后执行，请返回 actionCard 预览",
                    "tool_name": name,
                    "requires_confirmation": True,
                    "tool_args": args,
                })
                continue
            result = await registry.execute(name, args)
            results.append({
                "role": "tool",
                "content": result.content,
                "tool_name": name,
            })
        except Exception as e:
            logger.error("tool_execution_failed", extra={"tool": name, "error": str(e)})
            results.append({
                "role": "tool",
                "content": f"工具执行失败: {e}",
                "tool_name": name,
            })
    return results


async def agent_node(state: AgentState) -> AsyncIterator[str]:
    """
    Agent node with RAG retrieval and tool calling.

    Flow:
    1. Extract user query
    2. Retrieve relevant documents (RAG)
    3. Build system prompt with context + tool definitions
    4. Call LLM (with function calling support)
    5. If tool calls detected -> execute -> feed back to LLM
    6. Stream final response
    """
    try:
        agent_name = get_agent_name(state["assistant_id"])
        query = _extract_query(state["messages"])
        logger.info(f"agent_node started: assistant_id={state['assistant_id']}, agent_name={agent_name}")

        # Step 1: RAG retrieval
        context = await _retrieve_context(query, state["assistant_id"])

        # Step 2: Build system prompt
        system_prompt = get_system_prompt(agent_name, state["mode"], state.get("context"))
        if context:
            system_prompt += (
                "\n\n---\n\n"
                "[参考信息开始]\n"
                f"{context}\n"
                "[参考信息结束]\n\n"
                "请基于以上参考信息回答用户的问题。"
                "参考信息仅作参考，不得编造信息。"
                "如果参考信息不足以回答问题，请说明并给出通用建议。"
            )
        
        # 如果有页面上下文，添加到系统提示词
        if page_context := state.get("context"):
            from app.orchestrator.prompts import _format_context
            context_text = _format_context(page_context)
            if context_text:
                system_prompt += (
                    "\n\n---\n\n"
                    "[页面上下文开始]\n"
                    "以下是用户当前页面的数据，请基于这些数据回答问题：\n\n"
                    f"{context_text}\n"
                    "[页面上下文结束]\n\n"
                    "请基于以上页面上下文数据回答用户的问题。"
                    "如果上下文中有相关数据，请直接列出具体信息。"
                    "不要说'未收到'或'请提供'之类的话，数据已经在上下文中了。"
                )

        # Step 3: Get tool definitions for this agent
        registry = get_tools_for_agent(agent_name)
        tools = state["messages"]

        # Build messages with system prompt
        messages = [{"role": "system", "content": system_prompt}] + tools
        logger.info(f"agent_node: messages count={len(messages)}, system_prompt length={len(system_prompt)}")

        # Step 4: Call LLM
        llm = get_llm()
        logger.info(f"agent_node: using LLM provider={type(llm).__name__}")
        full_response = ""
        async for chunk in llm.stream(messages):
            full_response += chunk
            yield chunk

        # Step 5: Check for tool calls and execute if found (with iteration limit)
        iteration = 0
        while True:
            tool_calls = _parse_tool_calls(full_response)
            if not tool_calls or not registry or iteration >= MAX_ITERATIONS:
                break

            iteration += 1
            # Add assistant's response to conversation
            messages.append({"role": "assistant", "content": full_response})

            # Execute tools
            tool_results = await _execute_tools(tool_calls, agent_name)
            for tr in tool_results:
                messages.append(tr)
                yield tr["content"]

            # Second LLM call with tool results
            full_response = ""
            async for chunk in llm.stream(messages):
                full_response += chunk
                yield chunk

        if iteration >= MAX_ITERATIONS:
            yield "\n\n已达到最大迭代次数，无法继续处理。请简化您的请求。"
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"agent_node error: {e}\n{error_details}")
        # 重新抛出异常，让上层处理
        raise


# Router node
def router_node(state: AgentState) -> Literal["agent"]:
    """Route to the appropriate agent based on assistant_id."""
    return "agent"


# Build the graph using LangGraph
def build_graph():
    """
    Build the LangGraph workflow.

    Current flow: input -> agent_node (with RAG + tools) -> output
    Future: input -> router -> [task_agent, project_agent, coach_agent, file_agent, chat_agent] -> output
    """
    from langgraph.graph import StateGraph, END

    graph = StateGraph(AgentState)

    # Add the agent node (retrieval and tools are handled inside agent_node)
    graph.add_node("agent", lambda state: {"response_chunks": []})

    # Simple linear graph
    graph.set_entry_point("agent")
    graph.add_edge("agent", END)

    return graph.compile()
