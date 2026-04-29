"""
AI Orchestrator HTTP Client.
"""
import json
import logging
from typing import AsyncIterator

import httpx

from app.config.settings import settings

logger = logging.getLogger(__name__)


class AIClient:
    """HTTP client for ai-orchestrator service."""

    def __init__(self):
        self.base_url = settings.ai_orchestrator_url
        self.timeout = getattr(settings, "ai_orchestrator_timeout", 120)

    async def chat_stream(self, messages: list[dict], assistant_id: str, user_id: int, mode: str = "smart") -> AsyncIterator[dict]:
        """Stream chat response from AI orchestrator."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/ai/chat",
                    json={
                        "messages": messages,
                        "assistant_id": assistant_id,
                        "user_id": user_id,
                        "mode": mode,
                    },
                ) as resp:
                    async for line in resp.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            yield json.loads(data)
                        except json.JSONDecodeError:
                            continue
            except httpx.ConnectError:
                logger.warning("AI orchestrator not available, returning mock response")
                yield {"type": "token", "delta": "[Mock] AI orchestrator not available"}

    async def health_check(self) -> bool:
        """Check AI orchestrator health."""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.base_url}/health")
                return resp.status_code == 200
        except Exception:
            return False


ai_client = AIClient()
