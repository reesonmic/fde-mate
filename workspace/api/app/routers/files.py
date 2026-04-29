"""
Files Router - /api/v1/files/*
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.repositories.file_repo import FileRepository
from app.services.file_service import FileService
from app.schemas.file import (
    FileMetaDTO, UploadTokenRequest, UploadTokenResponse,
    FinalizeUploadRequest, FileQuery, FileTreeNode, QuotaDTO,
)

router = APIRouter()


def get_file_service(session: AsyncSession = Depends(get_async_session)) -> FileService:
    repo = FileRepository(session)
    return FileService(session, repo)


@router.get("")
async def list_files(query: FileQuery = Depends(), svc: FileService = Depends(get_file_service), user_id: int = 1):
    items, total = await svc.list_files(query, user_id)
    return {"items": items, "total": total}


@router.get("/tree", response_model=list[FileTreeNode])
async def file_tree(svc: FileService = Depends(get_file_service), user_id: int = 1):
    return await svc.get_tree(user_id)


@router.get("/quota", response_model=QuotaDTO)
async def get_quota(svc: FileService = Depends(get_file_service), user_id: int = 1):
    return await svc.get_quota(user_id)


@router.get("/{file_id}", response_model=FileMetaDTO)
async def get_file(file_id: int, svc: FileService = Depends(get_file_service), user_id: int = 1):
    return await svc.get_file(file_id, user_id)


@router.get("/{file_id}/download")
async def get_download_url(file_id: int, svc: FileService = Depends(get_file_service), user_id: int = 1):
    url = await svc.get_download_url(file_id, user_id)
    return {"url": url}


@router.post("/upload-token", response_model=UploadTokenResponse)
async def get_upload_token(req: UploadTokenRequest, svc: FileService = Depends(get_file_service), user_id: int = 1):
    return await svc.get_upload_token(req, user_id)


@router.post("/finalize-upload", response_model=FileMetaDTO)
async def finalize_upload(req: FinalizeUploadRequest, svc: FileService = Depends(get_file_service), user_id: int = 1):
    return await svc.finalize_upload(req, user_id)


@router.delete("/{file_id}")
async def delete_file(file_id: int, svc: FileService = Depends(get_file_service), user_id: int = 1):
    return await svc.delete_file(file_id, user_id)


@router.post("/batch-delete")
async def batch_delete(body: dict, svc: FileService = Depends(get_file_service), user_id: int = 1):
    return await svc.batch_delete(body.get("ids", []), user_id)
