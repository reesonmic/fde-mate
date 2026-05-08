"""  
Files Router - /api/v1/files/*
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.deps.auth import UserContext, current_user
from app.repositories.file_repo import FileRepository
from app.services.file_service import FileService
from app.schemas.file import (
    FileMetaDTO, UploadTokenRequest, UploadTokenResponse,
    FinalizeUploadRequest, FileQuery, FileTreeNode, QuotaDTO,
)

router = APIRouter()

# 文件上传大小限制：50MB
MAX_FILE_SIZE = 50 * 1024 * 1024


def get_file_service(session: AsyncSession = Depends(get_async_session)) -> FileService:
    repo = FileRepository(session)
    return FileService(session, repo)


class BatchDeleteRequest(BaseModel):
    ids: list[int] = []


@router.get("")
async def list_files(query: FileQuery = Depends(), svc: FileService = Depends(get_file_service), user: UserContext = Depends(current_user)):
    items, total = await svc.list_files(query, user.id)
    return {"items": items, "total": total}


@router.get("/tree", response_model=list[FileTreeNode])
async def file_tree(svc: FileService = Depends(get_file_service), user: UserContext = Depends(current_user)):
    return await svc.get_tree(user.id)


@router.get("/quota", response_model=QuotaDTO)
async def get_quota(svc: FileService = Depends(get_file_service), user: UserContext = Depends(current_user)):
    return await svc.get_quota(user.id)


@router.get("/{file_id}", response_model=FileMetaDTO)
async def get_file(file_id: int, svc: FileService = Depends(get_file_service), user: UserContext = Depends(current_user)):
    return await svc.get_file(file_id, user.id)


@router.get("/{file_id}/download")
async def get_download_url(file_id: int, svc: FileService = Depends(get_file_service), user: UserContext = Depends(current_user)):
    url = await svc.get_download_url(file_id, user.id)
    return {"url": url}


@router.post("/upload-token", response_model=UploadTokenResponse)
async def get_upload_token(req: UploadTokenRequest, svc: FileService = Depends(get_file_service), user: UserContext = Depends(current_user)):
    # 校验文件大小
    if req.file_size and req.file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail={
                "code": 6004,
                "message": f"文件大小超过限制（{MAX_FILE_SIZE // (1024*1024)}MB）"
            }
        )
    return await svc.get_upload_token(req, user.id)


@router.post("/finalize-upload", response_model=FileMetaDTO)
async def finalize_upload(req: FinalizeUploadRequest, svc: FileService = Depends(get_file_service), user: UserContext = Depends(current_user)):
    return await svc.finalize_upload(req, user.id)


@router.delete("/{file_id}")
async def delete_file(file_id: int, svc: FileService = Depends(get_file_service), user: UserContext = Depends(current_user)):
    return await svc.delete_file(file_id, user.id)


@router.post("/batch-delete")
async def batch_delete(req: BatchDeleteRequest, svc: FileService = Depends(get_file_service), user: UserContext = Depends(current_user)):
    return await svc.batch_delete(req.ids, user.id)
