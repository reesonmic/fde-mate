"""
Task schemas - TaskDTO, TaskCreate, TaskUpdate, TaskQuery, BatchUpdateStatusRequest.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.common import PageRequest


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    done = "done"
    blocked = "blocked"


class TaskPriority(str, Enum):
    p0 = "p0"
    p1 = "p1"
    p2 = "p2"
    p3 = "p3"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.p2
    assignee_id: int | None = Field(None, alias="assigneeId")
    project_id: int | None = Field(None, alias="projectId")
    due_at: datetime | None = Field(None, alias="dueAt")
    tags: list[str] = []

    model_config = {"populate_by_name": True}


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: int | None = Field(None, alias="assigneeId")
    due_at: datetime | None = Field(None, alias="dueAt")
    tags: list[str] | None = None

    model_config = {"populate_by_name": True}


class TaskDTO(TaskBase):
    id: int
    creator_id: int | None = None
    gmt_create: datetime = Field(alias="gmtCreate")
    gmt_modified: datetime = Field(alias="gmtModified")

    model_config = {"populate_by_name": True, "from_attributes": True}


class TaskQuery(PageRequest):
    keyword: str | None = None
    status: list[TaskStatus] | None = None
    assignee_id: int | None = Field(None, alias="assigneeId")
    project_id: int | None = Field(None, alias="projectId")
    priority: list[TaskPriority] | None = None

    model_config = {"populate_by_name": True}


class BatchUpdateStatusRequest(BaseModel):
    ids: list[int] = Field(..., min_length=1, max_length=200)
    status: TaskStatus
    action_id: str | None = Field(None, alias="actionId", description="Required when >10 items")

    model_config = {"populate_by_name": True}


class BatchAssignRequest(BaseModel):
    ids: list[int] = Field(..., min_length=1, max_length=200)
    assignee_id: int = Field(alias="assigneeId")

    model_config = {"populate_by_name": True}


class TaskCommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class TaskCommentDTO(BaseModel):
    id: int
    task_id: int
    user_id: int
    user_name: str
    content: str
    gmt_create: datetime = Field(alias="gmtCreate")

    model_config = {"populate_by_name": True}


class TaskHistoryDTO(BaseModel):
    id: int
    task_id: int
    user_id: int
    user_name: str
    op: str
    before: dict | None = None
    after: dict | None = None
    gmt_create: datetime = Field(alias="gmtCreate")

    model_config = {"populate_by_name": True}
