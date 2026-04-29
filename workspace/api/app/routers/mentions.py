"""
Mentions Router - /api/v1/mentions/search
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.services.mention_service import MentionService, MentionType

router = APIRouter()


def get_mention_service(session: AsyncSession = Depends(get_async_session)) -> MentionService:
    return MentionService(session)


@router.get("/search")
async def search_mentions(q: str, type: MentionType | None = None, limit: int = 10, svc: MentionService = Depends(get_mention_service)):
    return await svc.search(q, type, limit)
