from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from config.database import Base
import enum


class RoleEnum(str, enum.Enum):
    admin = "admin"
    professor = "professor"
    student = "student"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.student, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    enrollment = relationship("Enrollment", back_populates="student")
    course = relationship("Course", back_populates="professor")
