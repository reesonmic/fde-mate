"""
Coach schemas - BestPracticeDTO, SopDTO, LearningPathDTO, ChapterProgressUpdate.
"""
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import PageRequest


class BestPracticeDTO(BaseModel):
    id: int
    title: str
    scenario: str
    summary: str | None = None
    views: int = 0
    rating: float = 0.0
    gmt_create: datetime = Field(alias="gmtCreate")

    model_config = {"populate_by_name": True, "from_attributes": True}


class SopDTO(BaseModel):
    id: int
    title: str
    category: str
    summary: str | None = None
    downloads: int = 0
    rating: float = 0.0
    gmt_create: datetime = Field(alias="gmtCreate")

    model_config = {"populate_by_name": True, "from_attributes": True}


class ChapterDTO(BaseModel):
    id: int
    title: str
    sort_order: int = 0
    completed: bool = False
    progress: int = 0

    model_config = {"from_attributes": True}


class LearningPathDTO(BaseModel):
    id: int
    title: str
    description: str | None = None
    cover_url: str | None = None
    chapters: list[ChapterDTO] = []
    progress: int = 0
    gmt_create: datetime = Field(alias="gmtCreate")

    model_config = {"populate_by_name": True, "from_attributes": True}


class ChapterProgressUpdate(BaseModel):
    chapter_id: int
    progress: int = Field(ge=0, le=100)
    completed: bool = False


class CoachQuery(PageRequest):
    keyword: str | None = None
    scenario: str | None = None
    category: str | None = None


class RecommendationDTO(BaseModel):
    best_practices: list[BestPracticeDTO] = []
    sops: list[SopDTO] = []
    learning_paths: list[LearningPathDTO] = []


class CategoryDTO(BaseModel):
    """Coach分类DTO"""
    id: int
    name: str
    code: str
    description: str | None = None
    sort_order: int = 0
    icon: str | None = None

    model_config = {"from_attributes": True}


class ExpertDTO(BaseModel):
    """专家DTO"""
    id: int
    name: str
    title: str
    avatar: str | None = None
    specialties: list[str] = []
    rating: float = 0.0
    consultation_count: int = 0
    is_online: bool = False

    model_config = {"from_attributes": True}
