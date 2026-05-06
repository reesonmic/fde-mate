"""
AI Orchestrator request/response schemas.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    assistantId: str = Field(description="Assistant key: tasks/project/coach/files/chat")
    sessionId: str | None = None
    message: str = Field(..., min_length=1, max_length=8000)
    mode: Literal["smart", "creative", "rigorous"] = "smart"
    context: dict = Field(default_factory=dict)
    mentions: list[dict] = Field(default_factory=list)
    userId: int | None = None


class ChatTokenChunk(BaseModel):
    type: Literal["token"] = "token"
    delta: str


class ChatActionChunk(BaseModel):
    type: Literal["action"] = "action"
    actionId: str
    toolName: str
    params: dict
    preview: str
    severity: str = "low"


class ChatDoneChunk(BaseModel):
    type: Literal["done"] = "done"


class ChatErrorChunk(BaseModel):
    type: Literal["error"] = "error"
    message: str
