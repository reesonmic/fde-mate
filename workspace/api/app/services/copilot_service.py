"""
Copilot Service - SSE forwarding to ai-orchestrator + session management.
"""
import json
from typing import AsyncIterator

import httpx
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.models.ai import AiSession, AiMessage
from app.schemas.copilot import ChatRequest


class CopilotService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def chat_stream(self, req: ChatRequest, user_id: int) -> AsyncIterator[dict]:
        # Save user message
        await self._save_user_message(req, user_id)

        # Forward to ai-orchestrator
        async with httpx.AsyncClient(timeout=settings.ai_orchestrator_timeout) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{settings.ai_orchestrator_url}/ai/chat",
                    json={**req.model_dump(by_alias=True), "userId": user_id},
                    headers={"Content-Type": "application/json"},
                ) as upstream:
                    full_response = []
                    async for line in upstream.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            if chunk.get("type") == "token":
                                full_response.append(chunk["delta"])
                            yield chunk
                        except json.JSONDecodeError:
                            continue
            except httpx.ConnectError:
                # Fallback mock response when orchestrator is not available
                mock_text = f"[Mock AI] 收到消息: {req.message}"
                yield {"type": "token", "delta": mock_text}
                full_response = [mock_text]

        # Save assistant message
        await self._save_assistant_message(req, user_id, "".join(full_response))

    async def list_sessions(self, user_id: int) -> list[dict]:
        result = await self.session.execute(
            select(AiSession)
            .where(AiSession.user_id == user_id)
            .order_by(AiSession.gmt_modified.desc())
        )
        sessions = result.scalars().all()
        return [
            {
                "id": s.id,
                "assistant_key": s.assistant_key,
                "mode": s.mode,
                "title": s.title,
                "gmt_create": s.gmt_create.isoformat(),
            }
            for s in sessions
        ]

    async def get_session(self, session_id: int, user_id: int) -> dict | None:
        result = await self.session.execute(
            select(AiSession).where(AiSession.id == session_id, AiSession.user_id == user_id)
        )
        s = result.scalar_one_or_none()
        if not s:
            return None
        msg_result = await self.session.execute(
            select(AiMessage).where(AiMessage.session_id == session_id).order_by(AiMessage.gmt_create)
        )
        messages = msg_result.scalars().all()
        return {
            "id": s.id,
            "assistant_key": s.assistant_key,
            "mode": s.mode,
            "title": s.title,
            "messages": [
                {"role": m.role, "content": m.content, "gmt_create": m.gmt_create.isoformat()}
                for m in messages
            ],
        }

    async def delete_session(self, session_id: int, user_id: int) -> dict:
        result = await self.session.execute(
            select(AiSession).where(AiSession.id == session_id, AiSession.user_id == user_id)
        )
        s = result.scalar_one_or_none()
        if not s:
            return {"deleted": False}
        await self.session.delete(s)
        return {"deleted": True}

    async def _save_user_message(self, req: ChatRequest, user_id: int):
        session_id = None
        if req.session_id:
            session_id = int(req.session_id)
        if not session_id:
            session = AiSession(
                user_id=user_id,
                assistant_key=req.assistant_id,
                mode=req.mode,
                title=req.message[:50],
            )
            self.session.add(session)
            await self.session.flush()
            session_id = session.id
        msg = AiMessage(session_id=session_id, role="user", content=req.message)
        self.session.add(msg)
        await self.session.flush()

    async def _save_assistant_message(self, req: ChatRequest, user_id: int, content: str):
        session_id = int(req.session_id) if req.session_id else None
        if not session_id:
            return
        msg = AiMessage(session_id=session_id, role="assistant", content=content)
        self.session.add(msg)
        await self.session.flush()
