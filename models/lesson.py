from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(
        Integer,
        ForeignKey("courses.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String, nullable=False)
    content = Column(Text)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    course = relationship("Course", back_populates="lessons")
