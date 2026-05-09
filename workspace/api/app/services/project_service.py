"""
Project Service - CRUD + members + health + risks + weekly reports.
"""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.biz import ProjectNotFoundException, PermissionDeniedException
from app.models.project import Project
from app.repositories.project_repo import ProjectRepository
from app.schemas.common import PageResponse
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectDTO, ProjectQuery,
    MemberAdd, RiskCreate, ProjectMemberDTO, MilestoneDTO, RiskDTO,
    WeeklyReportDTO,
)


class ProjectService:
    def __init__(self, session: AsyncSession, repo: ProjectRepository):
        self.session = session
        self.repo = repo

    async def list_projects(self, query: ProjectQuery, user_id: int) -> PageResponse[ProjectDTO]:
        items, total = await self.repo.search(
            keyword=query.keyword,
            phase=[p.value for p in query.phase] if query.phase else None,
            owner_id=query.owner_id,
            viewer_id=user_id,
            page=query.page,
            size=query.size,
        )
        return PageResponse(
            items=[self._to_dto(p) for p in items],
            total=total, page=query.page, size=query.size,
        )

    async def get_project(self, project_id: int, user_id: int) -> ProjectDTO:
        project = await self.repo.get_with_relations(project_id)
        if not project or project.is_deleted:
            raise ProjectNotFoundException()
        # 权限检查：只有项目成员或所有者可以查看
        is_member = await self.repo.is_project_member(project_id, user_id)
        if project.owner_id != user_id and not is_member:
            raise PermissionDeniedException()
        return self._to_dto(project)

    async def create_project(self, payload: ProjectCreate, user_id: int) -> ProjectDTO:
        # 使用当前用户作为 owner（如果未指定）
        owner_id = payload.owner_id or user_id
        # 使用当前时间作为 start_at（如果未指定）
        start_at = payload.start_at or datetime.now()

        # 创建项目
        project = await self.repo.create(
            name=payload.name,
            customer_id=payload.customer_id,
            phase=payload.phase.value,
            owner_id=owner_id,
            start_at=start_at,
            end_at=payload.end_at,
        )
        # 添加创建者为项目成员
        await self.repo.add_member(project.id, owner_id, "owner")
        
        full = await self.repo.get_with_relations(project.id)
        return self._to_dto(full)

    async def update_project(self, project_id: int, payload: ProjectUpdate, user_id: int) -> ProjectDTO:
        project = await self.repo.get(project_id)
        if not project or project.is_deleted:
            raise ProjectNotFoundException()
        if project.owner_id != user_id:
            raise PermissionDeniedException()
        update_data = payload.model_dump(exclude_none=True)
        for k, v in update_data.items():
            setattr(project, k, v)
        await self.session.flush()
        full = await self.repo.get_with_relations(project_id)
        return self._to_dto(full)

    async def delete_project(self, project_id: int, user_id: int) -> dict:
        project = await self.repo.get(project_id)
        if not project:
            raise ProjectNotFoundException()
        if project.owner_id != user_id:
            raise PermissionDeniedException()
        await self.repo.soft_delete(project_id)
        return {"deleted": True}

    async def add_member(self, project_id: int, payload: MemberAdd, user_id: int) -> ProjectMemberDTO:
        project = await self.repo.get(project_id)
        if not project:
            raise ProjectNotFoundException()
        if project.owner_id != user_id:
            raise PermissionDeniedException()
        member = await self.repo.add_member(project_id, payload.user_id, payload.role.value)
        return self._member_to_dto(member)

    async def remove_member(self, project_id: int, user_id: int, target_user_id: int) -> dict:
        project = await self.repo.get(project_id)
        if not project or project.owner_id != user_id:
            raise PermissionDeniedException()
        removed = await self.repo.remove_member(project_id, target_user_id)
        if not removed:
            raise ProjectNotFoundException()
        return {"removed": True}

    async def get_members(self, project_id: int) -> list[ProjectMemberDTO]:
        members = await self.repo.get_members(project_id)
        return [self._member_to_dto(m) for m in members]

    async def add_risk(self, project_id: int, payload: RiskCreate, user_id: int) -> RiskDTO:
        project = await self.repo.get(project_id)
        if not project:
            raise ProjectNotFoundException()
        risk = await self.repo.add_risk(project_id, payload.title, payload.level.value, payload.mitigation)
        return self._risk_to_dto(risk)

    async def get_health(self, project_id: int) -> dict:
        project = await self.repo.get_with_relations(project_id)
        if not project:
            raise ProjectNotFoundException()
        # Simple health calculation
        health = project.health
        risk_count = len([r for r in project.risks if r.status == "open"])
        overdue = sum(1 for m in project.milestones if not m.done and m.due_at < datetime.utcnow())
        if risk_count > 3:
            health = max(0, health - 20)
        if overdue > 0:
            health = max(0, health - 10 * overdue)
        return {"health": health, "risk_count": risk_count, "overdue_milestones": overdue}

    async def get_weekly_reports(self, project_id: int) -> list[WeeklyReportDTO]:
        return []  # Placeholder - would need a weekly_report table

    async def generate_weekly_report(self, project_id: int, user_id: int) -> dict:
        # Trigger async report generation via Celery
        return {"status": "triggered"}

    def _to_dto(self, project: Project) -> ProjectDTO:
        return ProjectDTO(
            id=project.id,
            name=project.name,
            customer_id=project.customer_id,
            phase=project.phase,
            health=project.health,
            owner_id=project.owner_id,
            owner_name=project.owner.name if project.owner else None,
            start_at=project.start_at,
            end_at=project.end_at,
            members=[self._member_to_dto(m) for m in project.members],
            milestones=[MilestoneDTO(id=m.id, title=m.title, due_at=m.due_at, done=bool(m.done)) for m in project.milestones],
            risks=[self._risk_to_dto(r) for r in project.risks],
            gmt_create=project.gmt_create,
            gmt_modified=project.gmt_modified,
        )

    def _member_to_dto(self, member) -> ProjectMemberDTO:
        return ProjectMemberDTO(
            id=member.id,
            user_id=member.user_id,
            user_name=member.user.name if member.user else "",
            role=member.role,
        )

    def _risk_to_dto(self, risk) -> RiskDTO:
        return RiskDTO(
            id=risk.id,
            title=risk.title,
            level=risk.level,
            mitigation=risk.mitigation,
            status=risk.status,
        )
