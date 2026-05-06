"""
AI Orchestrator - FastAPI application entry point.

Provides HTTP endpoints for the AI orchestration service.
Called by the `api/` service - never accessed directly by `web/`.
"""
import json
import time
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.config import settings
from app.schemas import ChatRequest, ChatTokenChunk
from app.orchestrator.graph import agent_node, AgentState
from app.safety.input_guard import get_input_guard
from app.audit.logger import get_audit_logger, create_entry
from app.routing.router import get_router
from app.tools import get_all_tool_definitions

app = FastAPI(
    title="FDE AI Orchestrator",
    version="0.2.0",
    docs_url="/docs",
)

_input_guard = get_input_guard()
_audit = get_audit_logger()


class PreviewActionRequest(BaseModel):
    toolName: str = Field(..., min_length=1, max_length=100)
    args: dict = Field(default_factory=dict)


class ExecuteActionRequest(BaseModel):
    actionId: str = Field(..., min_length=1)


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": "0.2.0",
        "providers": get_router().get_provider_status(),
    }


@app.post("/ai/chat")
async def chat(req: ChatRequest) -> StreamingResponse:
    """
    SSE chat endpoint with safety guard and audit logging.
    Streams AI responses token by token.

    Called by the business API service at /api/v1/copilot/chat.
    """
    # Safety: check input
    safety = _input_guard.check(req.message)
    if not safety.is_safe:
        audit_entry = create_entry(
            user_id=req.userId,
            assistant_id=req.assistantId,
        )
        audit_entry.safety_triggered = True
        audit_entry.safety_reason = safety.reason
        audit_entry.input_preview = req.message[:100]
        _audit.log_safety_block(audit_entry)

        async def blocked_stream():
            yield "data: {\"type\": \"error\", \"message\": \"请求包含不安全的输入，已被系统拦截\"}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(
            blocked_stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache"},
        )

    # Create audit entry
    audit_entry = create_entry(
        user_id=req.userId,
        assistant_id=req.assistantId,
    )
    audit_entry.input_preview = req.message[:200]
    start_time = time.time()

    async def event_stream(request: Request) -> AsyncIterator[str]:
        state: AgentState = {
            "messages": [{"role": "user", "content": req.message}],
            "assistant_id": req.assistantId,
            "mode": req.mode,
            "context": req.context,
            "response_chunks": [],
        }

        full_response = ""
        try:
            async for chunk in agent_node(state):
                # Check client disconnect
                if await request.is_disconnected():
                    audit_entry.error = "client_disconnected"
                    break
                full_response += chunk
                data = ChatTokenChunk(delta=chunk).model_dump_json()
                yield f"data: {data}\n\n"
        except Exception as e:
            audit_entry.error = str(e)
            yield "data: {\"type\": \"error\", \"code\": \"BIZ_AI_INTERNAL_ERROR\", \"message\": \"AI 处理失败，请稍后重试\"}\n\n"

        # Audit log
        audit_entry.output_preview = full_response[:200]
        audit_entry.duration_ms = (time.time() - start_time) * 1000
        audit_entry.token_count = len(full_response)
        _audit.log_chat(audit_entry)

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(Request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/ai/tools")
async def list_tools(agent: str | None = None) -> dict:
    """List available tools for an agent or all agents."""
    return {"tools": get_all_tool_definitions(agent)}


@app.post("/ai/preview-action")
async def preview_action(req: PreviewActionRequest) -> dict:
    """Preview an AI action before execution."""
    tools = get_all_tool_definitions()
    return {
        "actionId": "preview-placeholder",
        "title": f"执行 {req.toolName}",
        "severity": "low",
        "preview": {"status": "preview", "toolName": req.toolName, "args": req.args},
        "availableTools": len(tools),
    }


@app.post("/ai/execute-action")
async def execute_action(req: ExecuteActionRequest) -> dict:
    """Execute a previously previewed action via actionId."""
    import redis.asyncio as redis
    from app.exceptions.codes import BIZ_AI_ACTION_NOT_FOUND, BIZ_AI_ACTION_EXPIRED

    try:
        r = redis.Redis(url=getattr(settings, "redis_url", "redis://localhost:6379/1"))
        action_data = await r.get(f"action:{req.actionId}")
        if action_data is None:
            await r.aclose()
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Action not found or expired")

        action_info = json.loads(action_data)
        await r.delete(f"action:{req.actionId}")
        await r.aclose()

        tool_name = action_info.get("tool_name", "")
        tool_args = action_info.get("args", {})

        from app.tools import get_tool_registry
        registry = get_tool_registry()
        result = await registry.execute(tool_name, tool_args)
        return {"success": True, "result": result}
    except HTTPException:
        raise
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Action execution failed: {e}")


@app.get("/ai/rag/search")
async def rag_search(query: str, top_k: int = 5) -> dict:
    """RAG search endpoint - combines Milvus + ES hybrid retrieval."""
    if not query or len(query) > 2000:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="query must be 1-2000 characters")
    if top_k < 1 or top_k > 50:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="top_k must be 1-50")

    from app.rag.retriever import get_retriever
    try:
        retriever = get_retriever()
        result = await retriever.retrieve(query, top_k=top_k)
        return {
            "results": [
                {"id": d.id, "content": d.content[:200], "score": d.score, "metadata": d.metadata}
                for d in result.documents
            ],
            "source": result.source,
        }
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"RAG search failed: {e}")
