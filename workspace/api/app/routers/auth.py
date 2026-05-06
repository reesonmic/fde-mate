"""
Auth Router - /api/v1/auth/*
"""
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.schemas.auth import LoginRequest, TokenPair, UserInfo
from app.services.auth_service import AuthService

router = APIRouter()


class RefreshRequest(BaseModel):
    refreshToken: str


@router.post("/login", response_model=TokenPair)
async def login(req: LoginRequest, session: AsyncSession = Depends(get_async_session)):
    svc = AuthService(session)
    return await svc.login(req)


@router.post("/refresh", response_model=TokenPair)
async def refresh(req: RefreshRequest, session: AsyncSession = Depends(get_async_session)):
    from app.services.auth_service import AuthService
    svc = AuthService(session)
    return await svc.refresh(req.refreshToken)


@router.post("/logout")
async def logout():
    return {"message": "登出成功"}


@router.get("/me", response_model=UserInfo)
async def get_me(authorization: str = Header(), session: AsyncSession = Depends(get_async_session)):
    from app.services.auth_service import AuthService
    token = authorization.replace("Bearer ", "")
    svc = AuthService(session)
    return await svc.get_current_user(token)
