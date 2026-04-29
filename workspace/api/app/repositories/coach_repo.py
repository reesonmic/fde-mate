"""
Coach Repository.
"""
from sqlalchemy import select, func
from app.models.coach import BestPractice, Sop, LearningPath, Chapter, UserChapterProgress
from app.repositories.base import BaseRepository


class CoachRepository(BaseRepository[BestPractice]):
    model = BestPractice

    async def search_practices(self, keyword: str | None = None, scenario: str | None = None,
                                page: int = 1, size: int = 20) -> tuple[list[BestPractice], int]:
        stmt = select(BestPractice).where(BestPractice.is_deleted == 0)
        if keyword:
            stmt = stmt.where(BestPractice.title.contains(keyword))
        if scenario:
            stmt = stmt.where(BestPractice.scenario == scenario)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.session.scalar(count_stmt) or 0

        stmt = stmt.order_by(BestPractice.rating.desc(), BestPractice.views.desc())
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def search_sops(self, keyword: str | None = None, category: str | None = None,
                          page: int = 1, size: int = 20) -> tuple[list[Sop], int]:
        stmt = select(Sop).where(Sop.is_deleted == 0)
        if keyword:
            stmt = stmt.where(Sop.title.contains(keyword))
        if category:
            stmt = stmt.where(Sop.category == category)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.session.scalar(count_stmt) or 0

        stmt = stmt.order_by(Sop.rating.desc(), Sop.downloads.desc())
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_learning_path(self, path_id: int) -> LearningPath | None:
        path = await self.session.get(LearningPath, path_id)
        if path:
            await self.session.refresh(path, ["chapters"])
        return path

    async def list_learning_paths(self, page: int = 1, size: int = 20) -> tuple[list[LearningPath], int]:
        stmt = select(LearningPath).where(LearningPath.is_deleted == 0)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.session.scalar(count_stmt) or 0
        stmt = stmt.order_by(LearningPath.gmt_create.desc())
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_user_progress(self, user_id: int, chapter_id: int) -> UserChapterProgress | None:
        result = await self.session.execute(
            select(UserChapterProgress).where(
                UserChapterProgress.user_id == user_id,
                UserChapterProgress.chapter_id == chapter_id,
            )
        )
        return result.scalar_one_or_none()

    async def update_progress(self, user_id: int, chapter_id: int, progress: int, completed: bool = False) -> UserChapterProgress:
        existing = await self.get_user_progress(user_id, chapter_id)
        if existing:
            existing.progress = progress
            existing.completed = int(completed)
            await self.session.flush()
            return existing
        else:
            p = UserChapterProgress(user_id=user_id, chapter_id=chapter_id, progress=progress, completed=int(completed))
            self.session.add(p)
            await self.session.flush()
            return p
