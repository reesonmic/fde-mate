"""
Coach models - best_practice + sop + learning_path + chapter tables.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin


class BestPractice(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "best_practice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    scenario = Column(String(100), nullable=False)
    summary = Column(Text)
    content = Column(Text)
    views = Column(Integer, nullable=False, default=0)
    rating = Column(Float, nullable=False, default=0.0)

    @property
    def rating_display(self) -> float:
        return round(self.rating, 1)


class Sop(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "sop"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    summary = Column(Text)
    content = Column(Text)
    downloads = Column(Integer, nullable=False, default=0)
    rating = Column(Float, nullable=False, default=0.0)


class LearningPath(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "learning_path"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    cover_url = Column(String(500))

    chapters = relationship("Chapter", back_populates="learning_path", order_by="Chapter.sort_order")


class Chapter(Base, TimestampMixin):
    __tablename__ = "chapter"

    id = Column(Integer, primary_key=True, autoincrement=True)
    learning_path_id = Column(Integer, ForeignKey("learning_path.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    sort_order = Column(Integer, nullable=False, default=0)
    required_chapter_id = Column(Integer, ForeignKey("chapter.id"))  # prerequisite

    learning_path = relationship("LearningPath", back_populates="chapters")
    required_chapter = relationship("Chapter", remote_side=[id])


class UserChapterProgress(Base, TimestampMixin):
    __tablename__ = "user_chapter_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("fde_user.id"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapter.id"), nullable=False)
    progress = Column(SmallInteger, nullable=False, default=0)  # 0-100
    completed = Column(SmallInteger, nullable=False, default=0)

    user = relationship("User")
    chapter = relationship("Chapter")
