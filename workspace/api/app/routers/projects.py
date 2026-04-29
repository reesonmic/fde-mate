"""
Projects Router - /api/v1/projects/*
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.repositories.project_repo import ProjectRepository
from app.services.project_service import ProjectService
from app.schemas.project import (
    ProjectDTO, ProjectCreate, ProjectUpdate, ProjectQuery,
    MemberAdd, RiskCreate, ProjectMemberDTO, RiskDTO,
)

router = APIRouter()


def get_project_service(session: AsyncSession = Depends(get_async_session)) -> ProjectService:
    repo = ProjectRepository(session)
    return ProjectService(session, repo)


@router.get("")
async def list_projects(query: ProjectQuery = Depends(), svc: ProjectService = Depends(get_project_service), user_id: int = 1):
    return await svc.list_projects(query, user_id)


@router.get("/{project_id}", response_model=ProjectDTO)
async def get_project(project_id: int, svc: ProjectService = Depends(get_project_service)):
    return await svc.get_project(project_id)


@router.post("", response_model=ProjectDTO)
async def create_project(payload: ProjectCreate, svc: ProjectService = Depends(get_project_service), user_id: int = 1):
    return await svc.create_project(payload, user_id)


@router.put("/{project_id}", response_model=ProjectDTO)
async def update_project(project_id: int, payload: ProjectUpdate, svc: ProjectService = Depends(get_project_service), user_id: int = 1):
    return await svc.update_project(project_id, payload, user_id)


@router.delete("/{project_id}")
async def delete_project(project_id: int, svc: ProjectService = Depends(get_project_service), user_id: int = 1):
    return await svc.delete_project(project_id, user_id)


@router.get("/{project_id}/members", response_model=list[ProjectMemberDTO])
async def get_members(project_id: int, svc: ProjectService = Depends(get_project_service)):
    return await svc.get_members(project_id)


@router.post("/{project_id}/members", response_model=ProjectMemberDTO)
async def add_member(project_id: int, payload: MemberAdd, svc: ProjectService = Depends(get_project_service), user_id: int = 1):
    return await svc.add_member(project_id, payload, user_id)


@router.delete("/{project_id}/members/{user_id}")
async def remove_member(project_id: int, user_id: int, svc: ProjectService = Depends(get_project_service), current_user_id: int = 1):
    return await svc.remove_member(project_id, current_user_id, user_id)


@router.get("/{project_id}/health")
async def get_health(project_id: int, svc: ProjectService = Depends(get_project_service)):
    return await svc.get_health(project_id)


@router.post("/{project_id}/risks", response_model=RiskDTO)
async def add_risk(project_id: int, payload: RiskCreate, svc: ProjectService = Depends(get_project_service), user_id: int = 1):
    return await svc.add_risk(project_id, payload, user_id)


@router.get("/{project_id}/weekly-reports")
async def weekly_reports(project_id: int, svc: ProjectService = Depends(get_project_service)):
    return await svc.get_weekly_reports(project_id)


@router.post("/{project_id}/weekly-reports")
async def generate_weekly_report(project_id: int, svc: ProjectService = Depends(get_project_service), user_id: int = 1):
    return await svc.generate_weekly_report(project_id, user_id)
