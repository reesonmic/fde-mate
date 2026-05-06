"""
Coach Router - /api/v1/coach/*
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.deps.auth import UserContext, current_user
from app.repositories.coach_repo import CoachRepository
from app.services.coach_service import CoachService
from app.schemas.coach import (
    BestPracticeDTO, SopDTO, LearningPathDTO, CoachQuery,
    ChapterProgressUpdate, RecommendationDTO,
)

router = APIRouter()


def get_coach_service(session: AsyncSession = Depends(get_async_session)) -> CoachService:
    repo = CoachRepository(session)
    return CoachService(session, repo)


class RatePracticeRequest(BaseModel):
    score: int = 5
    comment: str = ""


@router.get("/best-practices")
async def list_practices(query: CoachQuery = Depends(), svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.list_practices(query, user.id)


@router.get("/best-practices/{practice_id}", response_model=BestPracticeDTO)
async def get_practice(practice_id: int, svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.get_practice(practice_id, user.id)


@router.post("/best-practices/{practice_id}/rating")
async def rate_practice(practice_id: int, req: RatePracticeRequest, svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.rate_practice(practice_id, req.score, req.comment, user.id)


@router.get("/sops")
async def list_sops(query: CoachQuery = Depends(), svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.list_sops(query, user.id)


@router.get("/sops/{sop_id}", response_model=SopDTO)
async def get_sop(sop_id: int, svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.get_sop(sop_id, user.id)


@router.get("/sops/{sop_id}/download")
async def download_sop(sop_id: int, svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.download_sop(sop_id, user.id)


@router.get("/learning-paths")
async def list_learning_paths(page: int = 1, size: int = 20, svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.list_learning_paths(page, size, user.id)


@router.get("/learning-paths/{path_id}", response_model=LearningPathDTO)
async def get_learning_path(path_id: int, svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.get_learning_path(path_id, user.id)


@router.post("/learning-paths/{path_id}/progress")
async def update_progress(path_id: int, req: ChapterProgressUpdate, svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.update_chapter_progress(user.id, req)


@router.get("/recommendations", response_model=RecommendationDTO)
async def get_recommendations(svc: CoachService = Depends(get_coach_service), user: UserContext = Depends(current_user)):
    return await svc.get_recommendations(user.id)
