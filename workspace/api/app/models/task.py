"""
Task models - task + task_history tables.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin


class Task(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), nullable=False, default="todo")  # todo/in_progress/review/done/blocked
    priority = Column(String(10), nullable=False, default="p2")  # p0/p1/p2/p3
    assignee_id = Column(Integer, ForeignKey("fde_user.id"))
    project_id = Column(Integer, ForeignKey("project.id"))
    due_at = Column(DateTime)
    tags = Column(JSON, default=list)
    creator_id = Column(Integer, ForeignKey("fde_user.id"))

    # Relationships
    assignee = relationship("User", foreign_keys=[assignee_id])
    creator = relationship("User", foreign_keys=[creator_id])
    history = relationship("TaskHistory", back_populates="task", order_by="TaskHistory.gmt_create.desc()")


class TaskHistory(Base, TimestampMixin):
    __tablename__ = "task_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("fde_user.id"), nullable=False)
    op = Column(String(50), nullable=False)  # create/update/status_change
    before = Column(JSON)
    after = Column(JSON)

    task = relationship("Task", back_populates="history")
    user = relationship("User")
