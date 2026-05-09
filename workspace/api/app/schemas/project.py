"""
Project schemas - ProjectDTO, ProjectCreate, ProjectUpdate, MemberAdd, RiskCreate, etc.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.common import PageRequest


class ProjectPhase(str, Enum):
    init = "init"
    discovery = "discovery"
    delivery = "delivery"
    review = "review"
    closed = "closed"


class MemberRole(str, Enum):
    owner = "owner"
    core = "core"
    support = "support"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ProjectMemberDTO(BaseModel):
    id: int
    user_id: int
    user_name: str
    role: str

    model_config = {"from_attributes": True}


class MilestoneDTO(BaseModel):
    id: int
    title: str
    due_at: datetime = Field(alias="dueAt")
    done: bool

    model_config = {"populate_by_name": True, "from_attributes": True}

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            title=obj.title,
            due_at=obj.due_at,
            done=bool(obj.done),
            gmt_create=obj.gmt_create,
            gmt_modified=obj.gmt_modified,
        )


class RiskDTO(BaseModel):
    id: int
    title: str
    level: str
    mitigation: str | None = None
    status: str = "open"

    model_config = {"from_attributes": True}


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    customer_id: int | None = None
    phase: ProjectPhase = ProjectPhase.init
    owner_id: int | None = None  # 可选，默认使用当前用户
    start_at: datetime | None = None  # 可选，默认使用当前时间
    end_at: datetime | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    customer_id: int | None = None
    phase: ProjectPhase | None = None
    owner_id: int | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None


class MemberAdd(BaseModel):
    user_id: int
    role: MemberRole


class RiskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    level: RiskLevel
    mitigation: str | None = None


class ProjectDTO(BaseModel):
    id: int
    name: str
    customer_id: int | None = None
    phase: str
    health: int
    owner_id: int
    owner_name: str | None = None
    start_at: datetime
    end_at: datetime | None = None
    members: list[ProjectMemberDTO] = []
    milestones: list[MilestoneDTO] = []
    risks: list[RiskDTO] = []
    gmt_create: datetime = Field(alias="gmtCreate")
    gmt_modified: datetime = Field(alias="gmtModified")

    model_config = {"populate_by_name": True, "from_attributes": True}


class ProjectQuery(PageRequest):
    keyword: str | None = None
    phase: list[ProjectPhase] | None = None
    owner_id: int | None = None


class WeeklyReportDTO(BaseModel):
    id: int
    project_id: int
    week_start: datetime
    week_end: datetime
    content: str
    created_by: int
    gmt_create: datetime = Field(alias="gmtCreate")

    model_config = {"populate_by_name": True, "from_attributes": True}
