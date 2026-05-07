"""
AI Repository - encapsulates AiSession / AiMessage persistence so that
service layer never touches Session directly (M6-API-07).
"""
from sqlalchemy import select

from app.models.ai import AiMessage, AiSession
from app.repositories.base import BaseRepository


class AiSessionRepository(BaseRepository[AiSession]):
    model = AiSession

    async def list_by_user(self, user_id: int) -> list[AiSession]:
        result = await self.session.execute(
            select(AiSession)
            .where(AiSession.user_id == user_id)
            .order_by(AiSession.gmt_modified.desc())
        )
        return list(result.scalars().all())

    async def get_by_user(self, session_id: int, user_id: int) -> AiSession | None:
        result = await self.session.execute(
            select(AiSession).where(
                AiSession.id == session_id,
                AiSession.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_session(
        self,
        user_id: int,
        assistant_key: str,
        mode: str,
        title: str,
    ) -> AiSession:
        instance = AiSession(
            user_id=user_id,
            assistant_key=assistant_key,
            mode=mode,
            title=title,
        )
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def delete_session(self, session_id: int, user_id: int) -> bool:
        instance = await self.get_by_user(session_id, user_id)
        if not instance:
            return False
        await self.session.delete(instance)
        await self.session.flush()
        return True


class AiMessageRepository(BaseRepository[AiMessage]):
    model = AiMessage

    async def list_by_session(self, session_id: int) -> list[AiMessage]:
        result = await self.session.execute(
            select(AiMessage)
            .where(AiMessage.session_id == session_id)
            .order_by(AiMessage.gmt_create)
        )
        return list(result.scalars().all())

    async def append(
        self,
        session_id: int,
        role: str,
        content: str,
    ) -> AiMessage:
        msg = AiMessage(session_id=session_id, role=role, content=content)
        self.session.add(msg)
        await self.session.flush()
        return msg
