"""
Async task for RAG indexing.

M6-API-06:
Replaces the previous placeholder stub with a real httpx call to
ai-orchestrator's `/ai/rag/index` (M6-AI-05). On failure the task is
retried by Celery (autoretry_for + exponential backoff).
"""
import asyncio
import logging

import httpx

from app.config.settings import settings
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)

_AI_ORCH_BASE = getattr(settings, "ai_orchestrator_url", "http://localhost:8090")
_TIMEOUT = getattr(settings, "ai_orchestrator_timeout", 30)


async def _call_ai_orch_index(doc_id: str, content: str, metadata: dict) -> dict:
    """POST /ai/rag/index on ai-orchestrator. Raises on non-2xx."""
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.post(
            f"{_AI_ORCH_BASE}/ai/rag/index",
            json={"docId": doc_id, "content": content, "metadata": metadata},
        )
        resp.raise_for_status()
        return resp.json()


@celery_app.task(
    bind=True,
    autoretry_for=(httpx.HTTPError, httpx.ConnectError),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    max_retries=3,
)
def index_file_for_rag_task(
    self,
    file_id: int,
    content: str = "",
    metadata: dict | None = None,
):
    """
    Index a file for RAG retrieval by forwarding to ai-orchestrator.

    Args:
        file_id: business-side file id, used as docId
        content: text content extracted from the file (parser is upstream)
        metadata: optional fields like userId, projectId, fileType, etc.

    Returns:
        ai-orchestrator response payload, e.g. {"success": True, "docId": "..."}
    """
    doc_id = f"file:{file_id}"
    meta = metadata or {}

    if not content:
        # Nothing to index yet. Caller should provide parsed text; mark as skipped
        # so the upstream worker can decide whether to re-trigger after parsing.
        logger.warning("rag_index skipped: empty content for %s", doc_id)
        return {"docId": doc_id, "status": "skipped", "reason": "empty_content"}

    try:
        result = asyncio.run(_call_ai_orch_index(doc_id, content, meta))
    except httpx.HTTPStatusError as exc:
        # 4xx is non-retryable from the business perspective (bad payload).
        # 5xx will be retried by autoretry_for chain.
        logger.error(
            "rag_index http_error doc_id=%s status=%s body=%s",
            doc_id, exc.response.status_code, exc.response.text[:200],
        )
        if 400 <= exc.response.status_code < 500:
            return {"docId": doc_id, "status": "failed", "code": exc.response.status_code}
        raise

    return {"docId": doc_id, "status": "indexed", "ai_orch": result}


@celery_app.task(
    bind=True,
    autoretry_for=(httpx.HTTPError, httpx.ConnectError),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    max_retries=3,
)
def delete_file_from_rag_task(self, file_id: int):
    """Remove a file from the RAG store (used by file-delete flow)."""
    doc_id = f"file:{file_id}"

    async def _delete() -> dict:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.delete(f"{_AI_ORCH_BASE}/ai/rag/{doc_id}")
            resp.raise_for_status()
            return resp.json()

    try:
        result = asyncio.run(_delete())
    except httpx.HTTPStatusError as exc:
        logger.error(
            "rag_delete http_error doc_id=%s status=%s body=%s",
            doc_id, exc.response.status_code, exc.response.text[:200],
        )
        if 400 <= exc.response.status_code < 500:
            return {"docId": doc_id, "status": "failed", "code": exc.response.status_code}
        raise

    return {"docId": doc_id, "status": "deleted", "ai_orch": result}
