"""
File Repository.
"""
from sqlalchemy import select, func
from app.models.file import FileMeta
from app.repositories.base import BaseRepository


class FileRepository(BaseRepository[FileMeta]):
    model = FileMeta

    async def search(self, scope: str | None = None, scope_id: int | None = None,
                     keyword: str | None = None, ext: str | None = None,
                     owner_id: int | None = None, page: int = 1, size: int = 20) -> tuple[list[FileMeta], int]:
        stmt = select(FileMeta).where(FileMeta.is_deleted == 0)

        if scope:
            stmt = stmt.where(FileMeta.scope == scope)
        if scope_id:
            stmt = stmt.where(FileMeta.scope_id == scope_id)
        if keyword:
            stmt = stmt.where(FileMeta.name.contains(keyword))
        if ext:
            stmt = stmt.where(FileMeta.ext == ext)
        if owner_id:
            stmt = stmt.where(FileMeta.owner_id == owner_id)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.session.scalar(count_stmt) or 0

        stmt = stmt.order_by(FileMeta.gmt_create.desc())
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_tree(self, owner_id: int) -> list[FileMeta]:
        result = await self.session.execute(
            select(FileMeta).where(FileMeta.owner_id == owner_id, FileMeta.is_deleted == 0).order_by(FileMeta.name)
        )
        return list(result.scalars().all())

    async def get_quota(self, owner_id: int) -> int:
        from sqlalchemy import select as sl
        stmt = sl(func.sum(FileMeta.size)).where(FileMeta.owner_id == owner_id, FileMeta.is_deleted == 0)
        result = await self.session.scalar(stmt)
        return result or 0
