"""Tests for AI Orchestrator main app."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.schemas import ChatRequest


class TestHealthEndpoint:
    """TC-AI-HEALTH-001: Health check."""

    @pytest.mark.asyncio
    async def test_health_returns_ok(self):
        """Health endpoint should return ok status."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data


class TestChatEndpoint:
    """TC-AI-CHAT-001: Chat with SSE streaming."""

    @pytest.mark.asyncio
    async def test_chat_returns_sse_response(self):
        """Chat endpoint should return SSE stream."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/ai/chat",
                json={
                    "assistantId": "chat",
                    "message": "Hello",
                    "mode": "smart",
                },
            )

        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_chat_rejects_empty_message(self):
        """Chat endpoint should reject empty message."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/ai/chat",
                json={
                    "assistantId": "chat",
                    "message": "",
                },
            )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_chat_contains_done_marker(self):
        """Chat SSE stream should end with [DONE]."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/ai/chat",
                json={
                    "assistantId": "chat",
                    "message": "Test message",
                    "mode": "smart",
                },
            )

        content = response.text
        assert "[DONE]" in content

    @pytest.mark.asyncio
    async def test_chat_returns_token_chunks(self):
        """Chat SSE stream should return token chunks."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/ai/chat",
                json={
                    "assistantId": "chat",
                    "message": "What tasks do I have?",
                    "mode": "smart",
                },
            )

        content = response.text
        assert "data:" in content
        assert "type" in content


class TestPreviewActionEndpoint:
    """TC-AI-ACTION-001: Preview action."""

    @pytest.mark.asyncio
    async def test_preview_action_returns_response(self):
        """Preview action should return action card data."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/ai/preview-action",
                json={"toolName": "update_task", "args": {"status": "done"}},
            )

        assert response.status_code == 200
        data = response.json()
        assert "actionId" in data


class TestRagSearchEndpoint:
    """TC-AI-RAG-001: RAG search."""

    @pytest.mark.asyncio
    async def test_rag_search_returns_response(self):
        """RAG search should return empty results when not configured."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/ai/rag/search", params={"query": "test"})

        assert response.status_code == 200
        data = response.json()
        assert "results" in data


class TestPromptTemplates:
    """TC-AI-PROMPT-001: Prompt template management."""

    def test_get_system_prompt_for_task(self):
        """Should return task assistant prompt."""
        from app.orchestrator.prompts import get_system_prompt

        prompt = get_system_prompt("task")

        assert "任务" in prompt
        assert "T助手" in prompt

    def test_get_system_prompt_for_project(self):
        """Should return project assistant prompt."""
        from app.orchestrator.prompts import get_system_prompt

        prompt = get_system_prompt("project")

        assert "项目" in prompt
        assert "P助手" in prompt

    def test_get_system_prompt_for_coach(self):
        """Should return coach assistant prompt."""
        from app.orchestrator.prompts import get_system_prompt

        prompt = get_system_prompt("coach")

        assert "教练" in prompt
        assert "C助手" in prompt

    def test_get_system_prompt_for_file(self):
        """Should return file assistant prompt."""
        from app.orchestrator.prompts import get_system_prompt

        prompt = get_system_prompt("file")

        assert "文件" in prompt
        assert "F助手" in prompt

    def test_get_system_prompt_for_chat(self):
        """Should return chat assistant prompt."""
        from app.orchestrator.prompts import get_system_prompt

        prompt = get_system_prompt("chat")

        assert "AI" in prompt or "助手" in prompt

    def test_get_system_prompt_defaults_to_chat(self):
        """Unknown agent should default to chat prompt."""
        from app.orchestrator.prompts import get_system_prompt

        prompt = get_system_prompt("unknown")

        assert prompt is not None

    def test_get_system_prompt_includes_mode(self):
        """Should include mode in prompt."""
        from app.orchestrator.prompts import get_system_prompt

        prompt = get_system_prompt("task", mode="creative")

        assert "creative" in prompt


class TestLLMProvider:
    """TC-AI-LLM-001: LLM provider selection."""

    def test_mock_provider_returns_response(self):
        """Mock LLM should return a response."""
        from app.llm.provider import MockLlm
        import asyncio

        async def test_stream():
            llm = MockLlm()
            chunks = []
            async for chunk in llm.stream([{"role": "user", "content": "Hello"}]):
                chunks.append(chunk)

            return chunks

        chunks = asyncio.get_event_loop().run_until_complete(test_stream())
        assert len(chunks) > 0

    def test_mock_provider_handles_task_query(self):
        """Mock LLM should respond with task-related content."""
        from app.llm.provider import MockLlm
        import asyncio

        async def test_stream():
            llm = MockLlm()
            response = ""
            async for chunk in llm.stream([{"role": "user", "content": "任务"}]):
                response += chunk

            return response

        response = asyncio.get_event_loop().run_until_complete(test_stream())
        assert "任务" in response

    def test_mock_provider_handles_report_query(self):
        """Mock LLM should respond with report-related content."""
        from app.llm.provider import MockLlm
        import asyncio

        async def test_stream():
            llm = MockLlm()
            response = ""
            async for chunk in llm.stream([{"role": "user", "content": "周报"}]):
                response += chunk

            return response

        response = asyncio.get_event_loop().run_until_complete(test_stream())
        assert "周报" in response or "报告" in response


class TestGraph:
    """TC-AI-GRAPH-001: LangGraph orchestration."""

    def test_get_agent_name_mappings(self):
        """Should map assistant IDs to agent names."""
        from app.orchestrator.graph import get_agent_name

        assert get_agent_name("tasks") == "task"
        assert get_agent_name("task") == "task"
        assert get_agent_name("project") == "project"
        assert get_agent_name("coach") == "coach"
        assert get_agent_name("files") == "file"
        assert get_agent_name("chat") == "chat"
        assert get_agent_name("workspace") == "chat"
        assert get_agent_name("unknown") == "chat"
