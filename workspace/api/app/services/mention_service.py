"""
Mention Service - ES 5类对象搜索.
"""
from typing import Literal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.project import Project
from app.models.customer import Customer
from app.models.file import FileMeta
from app.models.coach import BestPractice

MentionType = Literal["task", "project", "customer", "file", "case"]


class MentionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(self, q: str, mention_type: MentionType | None = None, limit: int = 10) -> list[dict]:
        results = []
        types_to_search: list[MentionType] = [mention_type] if mention_type else ["task", "project", "customer", "file", "case"]

        for t in types_to_search:
            items = await self._search_type(t, q, limit)
            results.extend(items)

        return results[:limit * len(types_to_search)]

    async def _search_type(self, mention_type: MentionType, q: str, limit: int) -> list[dict]:
        if mention_type == "task":
            result = await self.session.execute(
                select(Task).where(Task.title.contains(q), Task.is_deleted == 0).limit(limit)
            )
            items = result.scalars().all()
            return [{"type": "task", "id": t.id, "title": t.title, "subtitle": f"状态: {t.status}"} for t in items]

        elif mention_type == "project":
            result = await self.session.execute(
                select(Project).where(Project.name.contains(q), Project.is_deleted == 0).limit(limit)
            )
            items = result.scalars().all()
            return [{"type": "project", "id": p.id, "title": p.name, "subtitle": f"阶段: {p.phase}"} for p in items]

        elif mention_type == "customer":
            result = await self.session.execute(
                select(Customer).where(Customer.name.contains(q), Customer.is_deleted == 0).limit(limit)
            )
            items = result.scalars().all()
            return [{"type": "customer", "id": c.id, "title": c.name, "subtitle": c.industry or ""} for c in items]

        elif mention_type == "file":
            result = await self.session.execute(
                select(FileMeta).where(FileMeta.name.contains(q), FileMeta.is_deleted == 0).limit(limit)
            )
            items = result.scalars().all()
            return [{"type": "file", "id": f.id, "title": f.name, "subtitle": f"{f.ext} · {f.size}B"} for f in items]

        elif mention_type == "case":
            result = await self.session.execute(
                select(BestPractice).where(BestPractice.title.contains(q), BestPractice.is_deleted == 0).limit(limit)
            )
            items = result.scalars().all()
            return [{"type": "case", "id": bp.id, "title": bp.title, "subtitle": bp.scenario} for bp in items]

        return []
