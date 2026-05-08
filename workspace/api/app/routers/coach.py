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
    CategoryDTO, ExpertDTO,
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


@router.get("/categories", response_model=list[CategoryDTO])
async def get_categories(user: UserContext = Depends(current_user)):
    """获取Coach分类列表"""
    # Mock数据 - 返回常见的FDE工作分类
    return [
        CategoryDTO(id=1, name="客户管理", code="customer", description="客户沟通与关系维护", sort_order=1, icon="UserGroup"),
        CategoryDTO(id=2, name="项目管理", code="project", description="项目交付与风险控制", sort_order=2, icon="Folder"),
        CategoryDTO(id=3, name="任务处理", code="task", description="任务分配与执行", sort_order=3, icon="CheckCircle"),
        CategoryDTO(id=4, name="文档规范", code="document", description="文档撰写与最佳实践", sort_order=4, icon="Document"),
        CategoryDTO(id=5, name="技术方案", code="technical", description="技术架构与解决方案", sort_order=5, icon="Code"),
    ]


@router.get("/experts", response_model=list[ExpertDTO])
async def get_experts(user: UserContext = Depends(current_user)):
    """获取专家列表"""
    # Mock数据 - 返回在线专家列表
    return [
        ExpertDTO(id=1, name="张专家", title="高级架构师", specialties=["云原生", "微服务"], rating=4.9, consultation_count=128, is_online=True),
        ExpertDTO(id=2, name="李顾问", title="项目管理专家", specialties=["敏捷开发", "风险管理"], rating=4.8, consultation_count=96, is_online=True),
        ExpertDTO(id=3, name="王工程师", title="资深FDE", specialties=["客户沟通", "需求分析"], rating=4.7, consultation_count=85, is_online=False),
    ]
