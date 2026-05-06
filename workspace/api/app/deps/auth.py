"""
Authentication Dependencies - async version.
"""
from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.models.user import User
from app.deps.db import get_async_session
from app.exceptions.biz import AuthException, PermissionDeniedException

security = HTTPBearer()


class UserContext:
    def __init__(self, id: int, name: str, email: str, roles: list[str], level: str):
        self.id = id
        self.name = name
        self.email = email
        self.roles = roles
        self.level = level


async def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session),
) -> UserContext:
    """Get current authenticated user from JWT token."""
    if not credentials.credentials:
        raise AuthException()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise AuthException()
    except JWTError:
        raise AuthException()

    result = await session.execute(select(User).where(User.id == int(user_id), User.is_deleted == 0))
    user = result.scalar_one_or_none()
    if not user:
        raise AuthException()

    return UserContext(
        id=user.id,
        name=user.name,
        email=user.email,
        roles=user.roles_list,
        level=user.level,
    )


def require_role(*roles: str):
    """Dependency factory that requires a specific role."""
    async def _checker(user: UserContext = Depends(current_user)):
        if not set(roles) & set(user.roles):
            raise PermissionDeniedException(f"Role(s) {roles} required")
        return user
    return _checker


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: AsyncSession = Depends(get_async_session),
) -> Optional[UserContext]:
    """Get current user if authenticated, otherwise return None."""
    if not credentials or not credentials.credentials:
        return None
    try:
        return await current_user(credentials, session)
    except Exception:
        return None
