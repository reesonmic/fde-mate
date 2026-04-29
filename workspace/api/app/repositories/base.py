"""
Base Repository with generic CRUD operations.
"""
from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> T | None:
        return await self.session.get(self.model, id)

    async def list_by_ids(self, ids: list[int]) -> list[T]:
        result = await self.session.execute(
            select(self.model).where(self.model.id.in_(ids))
        )
        return list(result.scalars().all())

    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def soft_delete(self, id: int) -> bool:
        instance = await self.get(id)
        if not instance:
            return False
        instance.is_deleted = 1  # type: ignore
        await self.session.flush()
        return True
