"""
File schemas - FileMetaDTO, UploadTokenResponse, FinalizeUploadRequest, FileTreeNode.
"""
from datetime import datetime

from pydantic import BaseModel, Field


class FileMetaDTO(BaseModel):
    id: int
    name: str
    ext: str
    size: int
    scope: str  # personal/project/customer/shared
    scope_id: int | None = None
    owner_id: int
    rag_indexed: bool = False
    gmt_create: datetime = Field(alias="gmtCreate")
    gmt_modified: datetime = Field(alias="gmtModified")

    model_config = {"populate_by_name": True, "from_attributes": True}


class UploadTokenRequest(BaseModel):
    file_name: str = Field(..., min_length=1, max_length=300)
    file_size: int
    scope: str = "personal"
    scope_id: int | None = None


class UploadTokenResponse(BaseModel):
    upload_token: str = Field(alias="uploadToken")
    oss_key: str = Field(alias="ossKey")
    endpoint: str
    bucket: str

    model_config = {"populate_by_name": True}


class FinalizeUploadRequest(BaseModel):
    oss_key: str = Field(alias="ossKey")
    file_name: str
    file_size: int
    scope: str = "personal"
    scope_id: int | None = None


class FileTreeNode(BaseModel):
    key: str
    title: str
    is_leaf: bool
    children: list["FileTreeNode"] = []


class FileQuery(BaseModel):
    scope: str | None = None
    scope_id: int | None = None
    keyword: str | None = None
    ext: str | None = None
    page: int = 1
    size: int = 20


class QuotaDTO(BaseModel):
    used_bytes: int
    total_bytes: int
    used_percent: float
