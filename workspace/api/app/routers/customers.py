"""
Customers Router - /api/v1/customers/*
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.deps.auth import UserContext, current_user
from app.repositories.customer_repo import CustomerRepository
from app.services.customer_service import CustomerService
from app.schemas.customer import (
    CustomerDTO, CustomerCreate, CustomerUpdate, CustomerQuery,
    ContactCreate, ContactDTO, OpportunityDTO,
)

router = APIRouter()


def get_customer_service(session: AsyncSession = Depends(get_async_session)) -> CustomerService:
    repo = CustomerRepository(session)
    return CustomerService(session, repo)


@router.get("")
async def list_customers(query: CustomerQuery = Depends(), svc: CustomerService = Depends(get_customer_service), user: UserContext = Depends(current_user)):
    return await svc.list_customers(query, user.id)


@router.get("/{customer_id}", response_model=CustomerDTO)
async def get_customer(customer_id: int, svc: CustomerService = Depends(get_customer_service), user: UserContext = Depends(current_user)):
    return await svc.get_customer(customer_id, user.id)


@router.post("", response_model=CustomerDTO)
async def create_customer(payload: CustomerCreate, svc: CustomerService = Depends(get_customer_service), user: UserContext = Depends(current_user)):
    return await svc.create_customer(payload, user.id)


@router.put("/{customer_id}", response_model=CustomerDTO)
async def update_customer(customer_id: int, payload: CustomerUpdate, svc: CustomerService = Depends(get_customer_service), user: UserContext = Depends(current_user)):
    return await svc.update_customer(customer_id, payload, user.id)


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int, svc: CustomerService = Depends(get_customer_service), user: UserContext = Depends(current_user)):
    return await svc.delete_customer(customer_id, user.id)


@router.get("/{customer_id}/contacts", response_model=list[ContactDTO])
async def get_contacts(customer_id: int, svc: CustomerService = Depends(get_customer_service), user: UserContext = Depends(current_user)):
    return await svc.get_contacts(customer_id, user.id)


@router.post("/{customer_id}/contacts", response_model=ContactDTO)
async def add_contact(customer_id: int, payload: ContactCreate, svc: CustomerService = Depends(get_customer_service), user: UserContext = Depends(current_user)):
    return await svc.add_contact(customer_id, payload, user.id)


@router.get("/{customer_id}/opportunities", response_model=list[OpportunityDTO])
async def get_opportunities(customer_id: int, svc: CustomerService = Depends(get_customer_service), user: UserContext = Depends(current_user)):
    return await svc.get_opportunities(customer_id, user.id)
