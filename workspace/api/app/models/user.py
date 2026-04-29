"""
User model - fde_user table.
"""
from sqlalchemy import Column, Integer, String, Text, SmallInteger
from app.models.base import Base, TimestampMixin, SoftDeleteMixin


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "fde_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    avatar = Column(String(500))
    roles = Column(String(200), nullable=False, default="fde")  # comma-separated: fde,tl,pm,admin
    level = Column(String(10), nullable=False, default="P5")  # P5-P9

    @property
    def roles_list(self) -> list[str]:
        return [r.strip() for r in self.roles.split(",") if r.strip()]
