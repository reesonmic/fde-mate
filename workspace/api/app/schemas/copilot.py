"""
Copilot schemas - ChatRequest, PreviewActionRequest/Response, ExecuteActionRequest/Response.
"""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


AssistantKey = Literal["workspace", "tasks", "project", "coach", "files", "chat"]


class ChatRequest(BaseModel):
    assistant_id: AssistantKey = Field(alias="assistantId")
    session_id: str | None = Field(None, alias="sessionId")
    message: str = Field(..., min_length=1, max_length=8000)
    context: dict = Field(default_factory=dict)
    mode: Literal["smart", "creative", "rigorous"] = "smart"
    mentions: list[dict] = []

    model_config = {"populate_by_name": True}


class PreviewActionRequest(BaseModel):
    tool_name: str = Field(alias="toolName")
    args: dict
    session_id: str = Field(alias="sessionId")

    model_config = {"populate_by_name": True}


class PreviewActionResponse(BaseModel):
    action_id: str = Field(alias="actionId")
    title: str
    severity: Literal["low", "medium", "high"]
    preview: dict
    affected_items: list[dict] | None = Field(None, alias="affectedItems")
    expires_at: datetime = Field(alias="expiresAt")

    model_config = {"populate_by_name": True}


class ExecuteActionRequest(BaseModel):
    action_id: str = Field(alias="actionId")

    model_config = {"populate_by_name": True}


class ExecuteActionResponse(BaseModel):
    success: bool
    result: dict


class CopilotSessionDTO(BaseModel):
    id: int
    assistant_key: str
    mode: str
    title: str | None = None
    message_count: int = 0
    gmt_create: datetime = Field(alias="gmtCreate")
    gmt_modified: datetime = Field(alias="gmtModified")

    model_config = {"populate_by_name": True, "from_attributes": True}


class CopilotFeedbackRequest(BaseModel):
    message_id: int = Field(alias="messageId")
    rating: Literal["up", "down"]

    model_config = {"populate_by_name": True}
