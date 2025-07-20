from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from schemas.user import UserResponse

if TYPE_CHECKING:
    from schemas.course import CourseResponse


class EnrollmentBase(BaseModel):
    enrolled_at: Optional[datetime] = None


class EnrollmentCreate(BaseModel):
    course_id: int
    student_id: int


class EnrollmentResponse(EnrollmentBase):
    id: int
    course: Optional["CourseResponse"] = None
    student: Optional[UserResponse] = None

    class Config:
        from_attributes = True
