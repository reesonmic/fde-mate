"""
Coach Service - cases/SOPs/learning paths + recommendations.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.coach_repo import CoachRepository
from app.schemas.common import PageResponse
from app.schemas.coach import (
    BestPracticeDTO, SopDTO, LearningPathDTO, CoachQuery,
    ChapterProgressUpdate, RecommendationDTO,
)


class CoachService:
    def __init__(self, session: AsyncSession, repo: CoachRepository):
        self.session = session
        self.repo = repo

    async def list_practices(self, query: CoachQuery) -> PageResponse[BestPracticeDTO]:
        items, total = await self.repo.search_practices(
            keyword=query.keyword,
            scenario=query.scenario,
            page=query.page,
            size=query.size,
        )
        return PageResponse(
            items=[BestPracticeDTO.model_validate(p, from_attributes=True) for p in items],
            total=total, page=query.page, size=query.size,
        )

    async def get_practice(self, practice_id: int) -> BestPracticeDTO:
        bp = await self.repo.get(practice_id)
        if not bp:
            from app.exceptions.biz import NotFoundException
            raise NotFoundException("BestPractice")
        bp.views += 1
        await self.session.flush()
        return BestPracticeDTO.model_validate(bp, from_attributes=True)

    async def list_sops(self, query: CoachQuery) -> PageResponse[SopDTO]:
        items, total = await self.repo.search_sops(
            keyword=query.keyword,
            category=query.category,
            page=query.page,
            size=query.size,
        )
        return PageResponse(
            items=[SopDTO.model_validate(s, from_attributes=True) for s in items],
            total=total, page=query.page, size=query.size,
        )

    async def get_sop(self, sop_id: int) -> SopDTO:
        from app.models.coach import Sop
        sop = await self.session.get(Sop, sop_id)
        if not sop:
            from app.exceptions.biz import NotFoundException
            raise NotFoundException("Sop")
        sop.downloads += 1
        await self.session.flush()
        return SopDTO.model_validate(sop, from_attributes=True)

    async def list_learning_paths(self, page: int = 1, size: int = 20, user_id: int | None = None) -> PageResponse[LearningPathDTO]:
        items, total = await self.repo.list_learning_paths(page=page, size=size)
        dtos = [self._path_to_dto(path) for path in items]
        return PageResponse(items=dtos, total=total, page=page, size=size)

    async def get_learning_path(self, path_id: int, user_id: int | None = None) -> LearningPathDTO:
        path = await self.repo.get_learning_path(path_id)
        if not path:
            from app.exceptions.biz import NotFoundException
            raise NotFoundException("LearningPath")
        return self._path_to_dto(path)

    async def update_chapter_progress(self, user_id: int, req: ChapterProgressUpdate) -> dict:
        await self.repo.update_progress(user_id, req.chapter_id, req.progress, req.completed)
        return {"updated": True}

    async def get_recommendations(self, user_id: int) -> RecommendationDTO:
        practices, _ = await self.repo.search_practices(page=1, size=5)
        sops, _ = await self.repo.search_sops(page=1, size=5)
        paths, _ = await self.repo.list_learning_paths(page=1, size=3)
        return RecommendationDTO(
            best_practices=[BestPracticeDTO.model_validate(p, from_attributes=True) for p in practices],
            sops=[SopDTO.model_validate(s, from_attributes=True) for s in sops],
            learning_paths=[self._path_to_dto(p) for p in paths],
        )

    def _path_to_dto(self, path) -> LearningPathDTO:
        chapters = [
            {"id": ch.id, "title": ch.title, "sort_order": ch.sort_order, "completed": False, "progress": 0}
            for ch in path.chapters
        ]
        return LearningPathDTO(
            id=path.id,
            title=path.title,
            description=path.description,
            cover_url=path.cover_url,
            chapters=chapters,
            progress=0,
            gmt_create=path.gmt_create,
        )
