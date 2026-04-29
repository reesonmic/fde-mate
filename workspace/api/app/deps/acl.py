"""
Access Control Dependencies.
"""
from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.auth import current_user, UserContext
from app.deps.db import get_async_session
from app.models.project import ProjectMember


async def require_project_access(
    project_id: int,
    user: UserContext = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> bool:
    """Check if user has access to a project."""
    result = await session.execute(
        select(func.count()).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user.id,
        )
    )
    count = result.scalar() or 0
    if count == 0:
        from app.exceptions.biz import PermissionDeniedException
        raise PermissionDeniedException()
    return True


async def require_customer_access(
    customer_id: int,
    user: UserContext = Depends(current_user),
) -> bool:
    """Check if user has access to a customer."""
    # All authenticated users can view customers
    return True
