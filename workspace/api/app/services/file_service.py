"""
File Service - metadata + OSS STS + quota.
"""
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.exceptions.biz import FileNotFoundException, PermissionDeniedException
from app.repositories.file_repo import FileRepository
from app.schemas.file import (
    FileMetaDTO, UploadTokenRequest, UploadTokenResponse,
    FinalizeUploadRequest, FileQuery, FileTreeNode, QuotaDTO,
)

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
QUOTA_LIMIT = 10 * 1024 * 1024 * 1024  # 10GB


class FileService:
    def __init__(self, session: AsyncSession, repo: FileRepository):
        self.session = session
        self.repo = repo

    async def list_files(self, query: FileQuery, user_id: int) -> tuple[list[FileMetaDTO], int]:
        items, total = await self.repo.search(
            scope=query.scope,
            scope_id=query.scope_id,
            keyword=query.keyword,
            ext=query.ext,
            owner_id=user_id,
            page=query.page,
            size=query.size,
        )
        return [FileMetaDTO.model_validate(f, from_attributes=True) for f in items], total

    async def get_file(self, file_id: int, user_id: int) -> FileMetaDTO:
        f = await self.repo.get(file_id)
        if not f or f.is_deleted:
            raise FileNotFoundException()
        if f.owner_id != user_id:
            raise PermissionDeniedException()
        return FileMetaDTO.model_validate(f, from_attributes=True)

    async def delete_file(self, file_id: int, user_id: int) -> dict:
        f = await self.repo.get(file_id)
        if not f:
            raise FileNotFoundException()
        if f.owner_id != user_id:
            raise PermissionDeniedException()
        await self.repo.soft_delete(file_id)
        return {"deleted": True}

    async def batch_delete(self, ids: list[int], user_id: int) -> dict:
        deleted = 0
        for fid in ids:
            f = await self.repo.get(fid)
            if f and f.owner_id == user_id:
                await self.repo.soft_delete(fid)
                deleted += 1
        return {"deleted": deleted}

    async def get_upload_token(self, req: UploadTokenRequest, user_id: int) -> UploadTokenResponse:
        used = await self.repo.get_quota(user_id)
        if used + req.file_size > QUOTA_LIMIT:
            raise PermissionDeniedException("存储配额已满")
        if req.file_size > MAX_FILE_SIZE:
            raise PermissionDeniedException("文件超过大小限制")

        ext = req.file_name.rsplit(".", 1)[-1] if "." in req.file_name else ""
        oss_key = f"uploads/{user_id}/{uuid.uuid4().hex}.{ext}"

        # Mock STS token - in production, use Aliyun STS SDK
        upload_token = f"mock-sts-token-{uuid.uuid4().hex}"

        return UploadTokenResponse(
            upload_token=upload_token,
            oss_key=oss_key,
            endpoint=settings.oss_endpoint or "https://oss-cn-hangzhou.aliyuncs.com",
            bucket=settings.oss_bucket or "fde-workspace",
        )

    async def finalize_upload(self, req: FinalizeUploadRequest, user_id: int) -> FileMetaDTO:
        ext = req.file_name.rsplit(".", 1)[-1] if "." in req.file_name else ""
        file_meta = await self.repo.create(
            name=req.file_name,
            ext=ext,
            size=req.file_size,
            scope=req.scope,
            scope_id=req.scope_id,
            owner_id=user_id,
            oss_key=req.oss_key,
            rag_indexed=0,
        )
        return FileMetaDTO.model_validate(file_meta, from_attributes=True)

    async def get_tree(self, user_id: int) -> list[FileTreeNode]:
        files = await self.repo.get_tree(user_id)
        # Group by scope
        scopes = {}
        for f in files:
            if f.scope not in scopes:
                scopes[f.scope] = []
            scopes[f.scope].append(FileTreeNode(key=f"file-{f.id}", title=f.name, is_leaf=True))
        return [
            FileTreeNode(key=f"scope-{k}", title=k, is_leaf=False, children=v)
            for k, v in scopes.items()
        ]

    async def get_quota(self, user_id: int) -> QuotaDTO:
        used = await self.repo.get_quota(user_id)
        return QuotaDTO(
            used_bytes=used,
            total_bytes=QUOTA_LIMIT,
            used_percent=round(used / QUOTA_LIMIT * 100, 2),
        )

    async def get_download_url(self, file_id: int, user_id: int) -> str:
        f = await self.repo.get(file_id)
        if not f or f.is_deleted:
            raise FileNotFoundException()
        if f.owner_id != user_id:
            raise PermissionDeniedException()
        # Mock download URL
        return f"https://{settings.oss_endpoint or 'oss.example.com'}/{settings.oss_bucket or 'fde'}/{f.oss_key}?expires=3600"
