"""
Common schemas - ApiResponse, PageRequest, PageResponse.
"""
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T | None = None
    trace_id: str | None = Field(default=None, alias="traceId")

    model_config = {"populate_by_name": True}


class PageRequest(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)


class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
