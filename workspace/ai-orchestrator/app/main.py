"""
AI Orchestrator - FastAPI application entry point.

Provides HTTP endpoints for the AI orchestration service.
Called by the `api/` service - never accessed directly by `web/`.

Architectural notes:
- Two-step write actions (preview-action / execute-action) are owned by the
  api layer's `ActionService`. Endpoints kept here are thin proxies that
  redirect callers to the api layer (M6-AI-01 / M6-AI-02).
- All non-SSE errors raise BizException / SystemException; HTTP responses
  are produced uniformly by `app.exceptions.handlers` (M6-AI-03).
- SSE error frames carry a stable `code` field so the frontend can
  classify failures (M6-AI-04).
"""
import json
import logging
import time
from typing import AsyncIterator

from fastapi import FastAPI, Request

logger = logging.getLogger(__name__)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.config import settings
from app.schemas import ChatRequest, ChatTokenChunk
from app.orchestrator.graph import agent_node, AgentState
from app.safety.input_guard import get_input_guard
from app.audit.logger import get_audit_logger, create_entry
from app.routing.router import get_router
from app.tools import get_all_tool_definitions
from app.exceptions import setup_exception_handlers
from app.exceptions.biz import (
    AIInvalidParamsException,
    AIRagSearchException,
)
from app.exceptions.codes import (
    BIZ_AI_PROMPT_INJECTION,
    BIZ_AI_ACTION_REQUIRED,
    BIZ_AI_RAG_INDEX_FAILED,
    SYS_INTERNAL_ERROR,
)

app = FastAPI(
    title="FDE AI Orchestrator",
    version="0.2.0",
    docs_url="/docs",
)

# Register unified exception handlers (M6-AI-03)
setup_exception_handlers(app)

_input_guard = get_input_guard()
_audit = get_audit_logger()


def _sse_error_frame(code: int, message: str) -> str:
    """Build an SSE error frame with a stable error code (M6-AI-04)."""
    payload = json.dumps(
        {"type": "error", "code": code, "message": message},
        ensure_ascii=False,
    )
    return f"data: {payload}\n\n"


class PreviewActionRequest(BaseModel):
    toolName: str = Field(..., min_length=1, max_length=100)
    args: dict = Field(default_factory=dict)


class ExecuteActionRequest(BaseModel):
    actionId: str = Field(..., min_length=1)

class RagIndexRequest(BaseModel):
    docId: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=200_000)
    metadata: dict = Field(default_factory=dict)


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": "0.2.0",
        "providers": get_router().get_provider_status(),
    }


@app.post("/ai/chat")
async def chat(request: Request, req: ChatRequest) -> StreamingResponse:
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
            yield _sse_error_frame(
                BIZ_AI_PROMPT_INJECTION,
                "请求包含不安全的输入，已被系统拦截",
            )
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

    async def event_stream() -> AsyncIterator[str]:
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
        except Exception as exc:  # noqa: BLE001
            # 记录详细的异常信息到日志
            import traceback
            error_details = traceback.format_exc()
            logger.error(f"AI chat error for assistant_id={req.assistantId}: {exc}\n{error_details}")
            
            audit_entry.error = str(exc)
            yield _sse_error_frame(
                SYS_INTERNAL_ERROR,
                "AI 处理失败，请稍后重试",
            )

        # Audit log
        audit_entry.output_preview = full_response[:200]
        audit_entry.duration_ms = (time.time() - start_time) * 1000
        audit_entry.token_count = len(full_response)
        _audit.log_chat(audit_entry)

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
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


# ---------- Two-step write actions (DEPRECATED here; owned by api layer) ----------
#
# M6-AI-01 / M6-AI-02:
# The actionId lifecycle (Redis cache, user/tool integrity check, TTL,
# audit binding) is owned by `api/app/services/action_service.py`.
# Keeping real implementations here would create two divergent sources of
# truth. These endpoints intentionally fail fast with a clear redirection
# message so any legacy direct caller is forced to migrate to:
#     POST /api/v1/copilot/preview-action
#     POST /api/v1/copilot/execute-action

@app.post("/ai/preview-action", deprecated=True)
async def preview_action(req: PreviewActionRequest) -> dict:
    """[DEPRECATED] actionId lifecycle is owned by api layer ActionService."""
    raise AIInvalidParamsException(
        message=(
            "ai-orchestrator no longer issues actionId. "
            "Call POST /api/v1/copilot/preview-action on the api service instead."
        ),
        details={
            "redirect": "/api/v1/copilot/preview-action",
            "toolName": req.toolName,
        },
    )


@app.post("/ai/execute-action", deprecated=True)
async def execute_action(req: ExecuteActionRequest) -> dict:
    """[DEPRECATED] actionId execution is owned by api layer ActionService."""
    raise AIInvalidParamsException(
        message=(
            "ai-orchestrator no longer executes actions. "
            "Call POST /api/v1/copilot/execute-action on the api service instead."
        ),
        details={
            "code": BIZ_AI_ACTION_REQUIRED,
            "redirect": "/api/v1/copilot/execute-action",
            "actionId": req.actionId,
        },
    )


@app.get("/ai/rag/search")
async def rag_search(query: str, top_k: int = 5) -> dict:
    """RAG search endpoint - combines Milvus + ES hybrid retrieval."""
    if not query or len(query) > 2000:
        raise AIInvalidParamsException("query must be 1-2000 characters")
    if top_k < 1 or top_k > 50:
        raise AIInvalidParamsException("top_k must be 1-50")

    from app.rag.retriever import get_retriever

    try:
        retriever = get_retriever()
        result = await retriever.retrieve(query, top_k=top_k)
    except Exception as exc:  # noqa: BLE001 - convert to domain exception
        raise AIRagSearchException(
            message="RAG retrieval failed",
            details={"reason": str(exc)},
        ) from exc

    return {
        "results": [
            {"id": d.id, "content": d.content[:200], "score": d.score, "metadata": d.metadata}
            for d in result.documents
        ],
        "source": result.source,
    }


# ---------- RAG indexing (M6-AI-05) ----------

@app.post("/ai/rag/index")
async def rag_index(req: RagIndexRequest) -> dict:
    """
    Index a document into the RAG store (Milvus + ES).

    Called by api layer Celery task `tasks.rag_index` after file upload
    or knowledge base content update.
    """
    from app.rag.retriever import get_retriever

    try:
        retriever = get_retriever()
        await retriever.index(
            doc_id=req.docId,
            content=req.content,
            metadata=req.metadata,
        )
    except AttributeError as exc:
        raise AIRagSearchException(
            message="RAG retriever does not expose index()",
            details={"reason": str(exc), "code": BIZ_AI_RAG_INDEX_FAILED},
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise AIRagSearchException(
            message="RAG index failed",
            details={"reason": str(exc), "code": BIZ_AI_RAG_INDEX_FAILED},
        ) from exc

    return {"success": True, "docId": req.docId}


@app.delete("/ai/rag/{doc_id}")
async def rag_delete(doc_id: str) -> dict:
    """Remove a document from the RAG store (used by file delete flow)."""
    if not doc_id or len(doc_id) > 200:
        raise AIInvalidParamsException("doc_id must be 1-200 characters")

    from app.rag.retriever import get_retriever

    try:
        retriever = get_retriever()
        await retriever.delete(doc_id=doc_id)
    except AttributeError as exc:
        raise AIRagSearchException(
            message="RAG retriever does not expose delete()",
            details={"reason": str(exc), "code": BIZ_AI_RAG_INDEX_FAILED},
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise AIRagSearchException(
            message="RAG delete failed",
            details={"reason": str(exc), "code": BIZ_AI_RAG_INDEX_FAILED},
        ) from exc

    return {"success": True, "docId": doc_id}
