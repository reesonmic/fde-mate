"""
Customer Repository.
"""
from sqlalchemy import select, func
from app.models.customer import Customer, Contact, Opportunity
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    model = Customer

    async def search(self, keyword: str | None = None, industry: str | None = None,
                     scale: str | None = None, page: int = 1, size: int = 20) -> tuple[list[Customer], int]:
        stmt = select(Customer).where(Customer.is_deleted == 0)
        if keyword:
            stmt = stmt.where(Customer.name.contains(keyword))
        if industry:
            stmt = stmt.where(Customer.industry == industry)
        if scale:
            stmt = stmt.where(Customer.scale == scale)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.session.scalar(count_stmt) or 0

        stmt = stmt.order_by(Customer.gmt_create.desc())
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_with_relations(self, customer_id: int) -> Customer | None:
        customer = await self.get(customer_id)
        if customer:
            await self.session.refresh(customer, ["contacts", "opportunities"])
        return customer

    async def add_contact(self, customer_id: int, **kwargs) -> Contact:
        contact = Contact(customer_id=customer_id, **kwargs)
        self.session.add(contact)
        await self.session.flush()
        return contact

    async def get_contacts(self, customer_id: int) -> list[Contact]:
        result = await self.session.execute(
            select(Contact).where(Contact.customer_id == customer_id, Contact.is_deleted == 0)
        )
        return list(result.scalars().all())

    async def get_opportunities(self, customer_id: int) -> list[Opportunity]:
        result = await self.session.execute(
            select(Opportunity).where(Opportunity.customer_id == customer_id, Opportunity.is_deleted == 0)
        )
        return list(result.scalars().all())

    # ---------- Dashboard helpers (M6-API-07) ----------

    async def count_active(self) -> int:
        return await self.session.scalar(
            select(func.count()).where(Customer.is_deleted == 0)
        ) or 0
