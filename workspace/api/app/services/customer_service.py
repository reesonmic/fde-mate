"""
Customer Service - CRUD + contacts + opportunities.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.biz import CustomerNotFoundException, PermissionDeniedException
from app.repositories.customer_repo import CustomerRepository
from app.schemas.common import PageResponse
from app.schemas.customer import (
    CustomerCreate, CustomerUpdate, CustomerDTO, CustomerQuery,
    ContactCreate, ContactDTO, OpportunityDTO,
)


class CustomerService:
    def __init__(self, session: AsyncSession, repo: CustomerRepository):
        self.session = session
        self.repo = repo

    async def list_customers(self, query: CustomerQuery) -> PageResponse[CustomerDTO]:
        items, total = await self.repo.search(
            keyword=query.keyword,
            industry=query.industry,
            scale=query.scale,
            page=query.page,
            size=query.size,
        )
        return PageResponse(
            items=[self._to_dto(c) for c in items],
            total=total, page=query.page, size=query.size,
        )

    async def get_customer(self, customer_id: int) -> CustomerDTO:
        customer = await self.repo.get_with_relations(customer_id)
        if not customer or customer.is_deleted:
            raise CustomerNotFoundException()
        return self._to_dto(customer)

    async def create_customer(self, payload: CustomerCreate) -> CustomerDTO:
        customer = await self.repo.create(
            name=payload.name,
            industry=payload.industry,
            scale=payload.scale,
            owner_id=payload.owner_id,
        )
        full = await self.repo.get_with_relations(customer.id)
        return self._to_dto(full)

    async def update_customer(self, customer_id: int, payload: CustomerUpdate) -> CustomerDTO:
        customer = await self.repo.get(customer_id)
        if not customer or customer.is_deleted:
            raise CustomerNotFoundException()
        update_data = payload.model_dump(exclude_none=True)
        for k, v in update_data.items():
            setattr(customer, k, v)
        await self.session.flush()
        full = await self.repo.get_with_relations(customer_id)
        return self._to_dto(full)

    async def delete_customer(self, customer_id: int) -> dict:
        customer = await self.repo.get(customer_id)
        if not customer:
            raise CustomerNotFoundException()
        await self.repo.soft_delete(customer_id)
        return {"deleted": True}

    async def add_contact(self, customer_id: int, payload: ContactCreate) -> ContactDTO:
        customer = await self.repo.get(customer_id)
        if not customer:
            raise CustomerNotFoundException()
        contact = await self.repo.add_contact(customer_id, **payload.model_dump())
        return self._contact_to_dto(contact)

    async def get_contacts(self, customer_id: int) -> list[ContactDTO]:
        contacts = await self.repo.get_contacts(customer_id)
        return [self._contact_to_dto(c) for c in contacts]

    async def get_opportunities(self, customer_id: int) -> list[OpportunityDTO]:
        opps = await self.repo.get_opportunities(customer_id)
        return [self._opp_to_dto(o) for o in opps]

    def _to_dto(self, customer) -> CustomerDTO:
        return CustomerDTO(
            id=customer.id,
            name=customer.name,
            industry=customer.industry,
            scale=customer.scale,
            owner_id=customer.owner_id,
            contacts=[self._contact_to_dto(c) for c in customer.contacts],
            opportunities=[self._opp_to_dto(o) for o in customer.opportunities],
            gmt_create=customer.gmt_create,
            gmt_modified=customer.gmt_modified,
        )

    def _contact_to_dto(self, contact) -> ContactDTO:
        return ContactDTO(
            id=contact.id,
            customer_id=contact.customer_id,
            name=contact.name,
            title=contact.title,
            phone=contact.phone,
            email=contact.email,
            gmt_create=contact.gmt_create,
        )

    def _opp_to_dto(self, opp) -> OpportunityDTO:
        return OpportunityDTO(
            id=opp.id,
            customer_id=opp.customer_id,
            title=opp.title,
            stage=opp.stage,
            amount=opp.amount,
            close_at=opp.close_at,
            gmt_create=opp.gmt_create,
        )
