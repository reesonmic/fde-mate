"""
Project Repository.
"""
from sqlalchemy import select, func
from app.models.project import Project, ProjectMember, Milestone, Risk
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    model = Project

    async def search(self, keyword: str | None = None, phase: list[str] | None = None,
                     owner_id: int | None = None, viewer_id: int | None = None,
                     page: int = 1, size: int = 20) -> tuple[list[Project], int]:
        from sqlalchemy.orm import joinedload
        
        # 使用 joinedload 预加载所有 relationship，避免懒加载导致 MissingGreenlet 错误
        stmt = select(Project).where(Project.is_deleted == 0).options(
            joinedload(Project.owner),
            joinedload(Project.members),
            joinedload(Project.milestones),
            joinedload(Project.risks),
        )

        if viewer_id:
            member_sub = select(ProjectMember.project_id).where(ProjectMember.user_id == viewer_id)
            stmt = stmt.where(
                (Project.owner_id == viewer_id) | (Project.id.in_(member_sub))
            )
        if keyword:
            stmt = stmt.where(Project.name.contains(keyword))
        if phase:
            stmt = stmt.where(Project.phase.in_(phase))
        if owner_id:
            stmt = stmt.where(Project.owner_id == owner_id)

        from sqlalchemy import select as sl
        count_stmt = sl(func.count()).select_from(stmt.subquery())
        total = await self.session.scalar(count_stmt) or 0

        stmt = stmt.order_by(Project.gmt_create.desc())
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        # 使用 unique() 处理 joinedload 可能产生的重复行
        return list(result.scalars().unique().all()), total

    async def get_with_relations(self, project_id: int) -> Project | None:
        from sqlalchemy.orm import joinedload
        
        # 使用 joinedload 预加载所有 relationship，避免懒加载
        stmt = select(Project).where(Project.id == project_id).options(
            joinedload(Project.owner),
            joinedload(Project.members),
            joinedload(Project.milestones),
            joinedload(Project.risks)
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def add_member(self, project_id: int, user_id: int, role: str) -> ProjectMember:
        member = ProjectMember(project_id=project_id, user_id=user_id, role=role)
        self.session.add(member)
        await self.session.flush()
        return member

    async def is_project_member(self, project_id: int, user_id: int) -> bool:
        """检查用户是否是项目成员"""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count()).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
        )
        return (result.scalar() or 0) > 0

    async def remove_member(self, project_id: int, user_id: int) -> bool:
        result = await self.session.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
        )
        member = result.scalar_one_or_none()
        if member:
            await self.session.delete(member)
            return True
        return False

    async def get_members(self, project_id: int) -> list[ProjectMember]:
        result = await self.session.execute(
            select(ProjectMember).where(ProjectMember.project_id == project_id)
        )
        return list(result.scalars().all())

    async def add_milestone(self, project_id: int, title: str, due_at, done: bool = False) -> Milestone:
        ms = Milestone(project_id=project_id, title=title, due_at=due_at, done=int(done))
        self.session.add(ms)
        await self.session.flush()
        return ms

    async def add_risk(self, project_id: int, title: str, level: str, mitigation: str | None = None) -> Risk:
        risk = Risk(project_id=project_id, title=title, level=level, mitigation=mitigation)
        self.session.add(risk)
        await self.session.flush()
        return risk

    async def get_risks(self, project_id: int) -> list[Risk]:
        result = await self.session.execute(
            select(Risk).where(Risk.project_id == project_id)
        )
        return list(result.scalars().all())

    # ---------- Dashboard helpers (M6-API-07) ----------

    async def count_by_owner(self, owner_id: int) -> int:
        return await self.session.scalar(
            select(func.count()).where(
                Project.is_deleted == 0, Project.owner_id == owner_id
            )
        ) or 0

    async def list_recent_by_owner(self, owner_id: int, limit: int) -> list[Project]:
        result = await self.session.execute(
            select(Project)
            .where(Project.is_deleted == 0, Project.owner_id == owner_id)
            .order_by(Project.gmt_create.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
