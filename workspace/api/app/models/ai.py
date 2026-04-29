"""
AI models - ai_session + ai_message tables.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class AiSession(Base, TimestampMixin):
    __tablename__ = "ai_session"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("fde_user.id"), nullable=False)
    assistant_key = Column(String(50), nullable=False)  # workspace/tasks/project/coach/files/chat
    mode = Column(String(20), nullable=False, default="smart")  # smart/creative/rigorous
    title = Column(String(200))

    user = relationship("User")
    messages = relationship("AiMessage", back_populates="session", order_by="AiMessage.gmt_create")


class AiMessage(Base, TimestampMixin):
    __tablename__ = "ai_message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("ai_session.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user/assistant/system
    content = Column(Text)
    card_data = Column(String(2000))  # JSON string for card data

    session = relationship("AiSession", back_populates="messages")
