"""
Settings Router - /api/v1/settings/*
"""
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/profile")
async def get_profile(user_id: int = 1):
    return {
        "id": user_id,
        "name": "FDE User",
        "email": "user@example.com",
        "avatar": None,
        "level": "P6",
    }


@router.put("/profile")
async def update_profile(body: dict, user_id: int = 1):
    return {"updated": True}


@router.put("/password")
async def change_password(body: dict, user_id: int = 1):
    return {"updated": True}


@router.get("/notifications")
async def get_notifications(user_id: int = 1):
    return {
        "dingtalk_enabled": True,
        "email_enabled": False,
        "in_app_enabled": True,
    }


@router.put("/notifications")
async def update_notifications(body: dict, user_id: int = 1):
    return {"updated": True}


@router.get("/ai-models")
async def get_ai_models(user_id: int = 1):
    return {
        "models": [
            {"id": "dashscope", "name": "通义千问", "enabled": True},
            {"id": "openai", "name": "GPT-4", "enabled": False},
        ],
        "preferred": "dashscope",
    }


@router.put("/ai-models")
async def set_ai_model(body: dict, user_id: int = 1):
    return {"updated": True}
