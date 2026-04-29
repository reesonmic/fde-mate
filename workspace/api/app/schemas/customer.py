"""
Customer schemas - CustomerDTO, ContactCreate, OpportunityDTO.
"""
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.common import PageRequest


class ContactDTO(BaseModel):
    id: int
    customer_id: int
    name: str
    title: str | None = None
    phone: str | None = None
    email: str | None = None
    gmt_create: datetime = Field(alias="gmtCreate")

    model_config = {"populate_by_name": True, "from_attributes": True}


class ContactCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    title: str | None = None
    phone: str | None = None
    email: str | None = None


class OpportunityDTO(BaseModel):
    id: int
    customer_id: int
    title: str
    stage: str
    amount: Decimal | None = None
    close_at: datetime | None = None
    gmt_create: datetime = Field(alias="gmtCreate")

    model_config = {"populate_by_name": True, "from_attributes": True}


class CustomerDTO(BaseModel):
    id: int
    name: str
    industry: str | None = None
    scale: str | None = None
    owner_id: int | None = None
    contacts: list[ContactDTO] = []
    opportunities: list[OpportunityDTO] = []
    gmt_create: datetime = Field(alias="gmtCreate")
    gmt_modified: datetime = Field(alias="gmtModified")

    model_config = {"populate_by_name": True, "from_attributes": True}


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    industry: str | None = None
    scale: str | None = None
    owner_id: int | None = None


class CustomerUpdate(BaseModel):
    name: str | None = None
    industry: str | None = None
    scale: str | None = None
    owner_id: int | None = None


class CustomerQuery(PageRequest):
    keyword: str | None = None
    industry: str | None = None
    scale: str | None = None
