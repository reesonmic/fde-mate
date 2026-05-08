"""
Authentication Service - login/token/password.
"""
from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt, JWTError
import bcrypt
from sqlalchemy import select

from app.config.settings import settings
from app.deps.db import get_async_session
from app.exceptions.biz import AuthException, TokenInvalidException
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenPair, UserInfo


class AuthService:
    def __init__(self, session):
        self.session = session

    async def login(self, req: LoginRequest) -> TokenPair:
        identifier = req.get_identifier()
        if not identifier:
            raise AuthException("请输入用户名或邮箱")
        
        # Try to find user by email or username
        result = await self.session.execute(
            select(User).where(
                (User.email == identifier) | (User.name == identifier),
                User.is_deleted == 0
            )
        )
        user = result.scalar_one_or_none()
        
        if not user or not bcrypt.checkpw(req.password.get_secret_value().encode(), user.password_hash.encode()):
            raise AuthException("用户名或密码错误")
        
        return await self._create_token_pair(user)

    async def refresh(self, refresh_token: str) -> TokenPair:
        try:
            payload = jwt.decode(refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            if payload.get("type") != "refresh":
                raise TokenInvalidException()
            user_id = int(payload.get("sub"))
        except JWTError:
            raise TokenInvalidException()

        result = await self.session.execute(select(User).where(User.id == user_id, User.is_deleted == 0))
        user = result.scalar_one_or_none()
        if not user:
            raise TokenInvalidException()
        return await self._create_token_pair(user)

    async def get_current_user(self, token: str) -> UserInfo:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            if payload.get("type") != "access":
                raise TokenInvalidException()
            user_id = int(payload.get("sub"))
        except JWTError:
            raise TokenInvalidException()

        result = await self.session.execute(select(User).where(User.id == user_id, User.is_deleted == 0))
        user = result.scalar_one_or_none()
        if not user:
            raise AuthException()
        return UserInfo(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar=user.avatar,
            roles=user.roles_list,
            level=user.level,
        )

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    async def _create_token_pair(self, user: User) -> TokenPair:
        now = datetime.utcnow()
        access_exp = now + timedelta(minutes=settings.jwt_expire_minutes)
        refresh_exp = now + timedelta(days=7)

        access_payload = {
            "sub": str(user.id),
            "type": "access",
            "roles": user.roles,
            "exp": access_exp,
        }
        refresh_payload = {
            "sub": str(user.id),
            "type": "refresh",
            "exp": refresh_exp,
        }

        access_token = jwt.encode(access_payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        refresh_token = jwt.encode(refresh_payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.jwt_expire_minutes * 60,
        )


def get_auth_service(session=Depends(get_async_session)) -> AuthService:
    return AuthService(session)
