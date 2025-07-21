from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from schemas.user import UserNameOnly
from schemas.lesson import LessonResponse
from schemas.enrollment import EnrollmentResponse


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    professor: Optional[UserNameOnly] = None
    # lessons: Optional[List[LessonResponse]] = []
    # enrollments: Optional[List[EnrollmentResponse]] = []

    class Config:
        from_attributes = True
