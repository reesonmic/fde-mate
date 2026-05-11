"""
Copilot Service - SSE forwarding to ai-orchestrator + session management.
"""
import json
from typing import AsyncIterator

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.repositories.ai_repo import AiMessageRepository, AiSessionRepository
from app.schemas.copilot import ChatRequest


class CopilotService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.session_repo = AiSessionRepository(session)
        self.message_repo = AiMessageRepository(session)

    async def chat_stream(self, req: ChatRequest, user_id: int) -> AsyncIterator[dict]:
        # Save user message
        await self._save_user_message(req, user_id)

        # Forward to ai-orchestrator
        full_response = []
        async with httpx.AsyncClient(timeout=settings.ai_orchestrator_timeout) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{settings.ai_orchestrator_url}/ai/chat",
                    json={**req.model_dump(by_alias=True), "userId": user_id},
                    headers={"Content-Type": "application/json"},
                ) as upstream:
                    async for line in upstream.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            # 检查是否是错误响应
                            if chunk.get("type") == "error":
                                # AI Orchestrator 返回错误，使用 mock 回复
                                mock_text = f"[AI 服务异常] {chunk.get('message', 'AI 处理失败，已降级为 Mock 回复')}\n\n您的消息是：{req.message}"
                                yield {"type": "token", "delta": mock_text}
                                full_response.append(mock_text)
                            elif chunk.get("type") == "token":
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
        sessions = await self.session_repo.list_by_user(user_id)
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
        s = await self.session_repo.get_by_user(session_id, user_id)
        if not s:
            return None
        messages = await self.message_repo.list_by_session(session_id)
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
        deleted = await self.session_repo.delete_session(session_id, user_id)
        return {"deleted": deleted}

    async def _save_user_message(self, req: ChatRequest, user_id: int):
        # Try to parse session_id as int, ignore if it's a string like 'chat-session-xxx'
        session_id: int | None = None
        if req.session_id:
            try:
                session_id = int(req.session_id)
            except (ValueError, TypeError):
                session_id = None
        
        if not session_id:
            new_session = await self.session_repo.create_session(
                user_id=user_id,
                assistant_key=req.assistant_id,
                mode=req.mode,
                title=req.message[:50],
            )
            session_id = new_session.id
        await self.message_repo.append(
            session_id=session_id, role="user", content=req.message
        )

    async def _save_assistant_message(self, req: ChatRequest, user_id: int, content: str):
        # Try to parse session_id as int, ignore if it's a string
        session_id: int | None = None
        if req.session_id:
            try:
                session_id = int(req.session_id)
            except (ValueError, TypeError):
                session_id = None
        
        if not session_id:
            return
        await self.message_repo.append(
            session_id=session_id, role="assistant", content=content
        )
