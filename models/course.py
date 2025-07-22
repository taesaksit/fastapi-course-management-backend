from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    professor_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    professor = relationship("User", back_populates="course")
    lessons = relationship(
        "Lesson",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    enrollment = relationship("Enrollment", back_populates="course")
