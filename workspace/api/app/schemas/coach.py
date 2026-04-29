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
