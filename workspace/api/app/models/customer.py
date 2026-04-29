"""
Customer models - customer + contact + opportunity tables.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Numeric
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin


class Customer(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    industry = Column(String(100))
    scale = Column(String(20))  # sme/large/kabp
    owner_id = Column(Integer, ForeignKey("fde_user.id"))

    owner = relationship("User")
    contacts = relationship("Contact", back_populates="customer", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="customer", cascade="all, delete-orphan")


class Contact(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    name = Column(String(100), nullable=False)
    title = Column(String(100))
    phone = Column(String(30))
    email = Column(String(200))

    customer = relationship("Customer", back_populates="contacts")


class Opportunity(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "opportunity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    title = Column(String(200), nullable=False)
    stage = Column(String(50), nullable=False)
    amount = Column(Numeric(12, 2))
    close_at = Column(DateTime)

    customer = relationship("Customer", back_populates="opportunities")
