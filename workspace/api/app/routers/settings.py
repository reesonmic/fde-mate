"""
Settings Router - /api/v1/settings/*
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.deps.auth import UserContext, current_user

router = APIRouter()


class ProfileUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    avatar: str | None = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class NotificationSettings(BaseModel):
    dingtalk_enabled: bool | None = None
    email_enabled: bool | None = None
    in_app_enabled: bool | None = None


class AIModelSettings(BaseModel):
    preferred: str


@router.get("/profile")
async def get_profile(user: UserContext = Depends(current_user)):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "avatar": None,
        "level": user.level,
    }


@router.put("/profile")
async def update_profile(payload: ProfileUpdate, user: UserContext = Depends(current_user)):
    return {"updated": True, "userId": user.id}


@router.put("/password")
async def change_password(payload: PasswordChange, user: UserContext = Depends(current_user)):
    return {"updated": True, "userId": user.id}


@router.get("/notifications")
async def get_notifications(user: UserContext = Depends(current_user)):
    return {
        "dingtalk_enabled": True,
        "email_enabled": False,
        "in_app_enabled": True,
    }


@router.put("/notifications")
async def update_notifications(payload: NotificationSettings, user: UserContext = Depends(current_user)):
    return {"updated": True, "userId": user.id}


@router.get("/ai-models")
async def get_ai_models(user: UserContext = Depends(current_user)):
    return {
        "models": [
            {"id": "dashscope", "name": "通义千问", "enabled": True},
            {"id": "openai", "name": "GPT-4", "enabled": False},
        ],
        "preferred": "dashscope",
    }


@router.put("/ai-models")
async def set_ai_model(payload: AIModelSettings, user: UserContext = Depends(current_user)):
    return {"updated": True, "preferred": payload.preferred}
