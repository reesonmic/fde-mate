"""
Project models - project + project_member + milestone + risk tables.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin


class Project(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    phase = Column(String(30), nullable=False, default="init")  # init/discovery/delivery/review/closed
    health = Column(Integer, nullable=False, default=100)  # 0-100
    owner_id = Column(Integer, ForeignKey("fde_user.id"))
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime)

    owner = relationship("User")
    customer = relationship("Customer")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="project", cascade="all, delete-orphan")


class ProjectMember(Base, TimestampMixin):
    __tablename__ = "project_member"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("fde_user.id"), nullable=False)
    role = Column(String(20), nullable=False)  # owner/core/support

    project = relationship("Project", back_populates="members")
    user = relationship("User")


class Milestone(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "milestone"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    title = Column(String(200), nullable=False)
    due_at = Column(DateTime, nullable=False)
    done = Column(SmallInteger, nullable=False, default=0)

    project = relationship("Project", back_populates="milestones")


class Risk(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "risk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    title = Column(String(200), nullable=False)
    level = Column(String(20), nullable=False)  # low/medium/high
    mitigation = Column(Text)
    status = Column(String(20), nullable=False, default="open")  # open/mitigated/closed

    project = relationship("Project", back_populates="risks")
