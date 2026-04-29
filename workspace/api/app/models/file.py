"""
File model - file_meta table.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin


class FileMeta(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "file_meta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)
    ext = Column(String(20), nullable=False)
    size = Column(BigInteger, nullable=False)
    scope = Column(String(30), nullable=False)  # personal/project/customer/shared
    scope_id = Column(Integer)
    owner_id = Column(Integer, ForeignKey("fde_user.id"))
    oss_key = Column(String(500), nullable=False)
    rag_indexed = Column(SmallInteger, nullable=False, default=0)

    owner = relationship("User")
