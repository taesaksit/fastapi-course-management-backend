from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.user import UserResponse


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    professor: Optional[UserResponse] = None
    # lessons: Optional[List[LessonResponse]] = []
    # enrollments: Optional[List["EnrollmentResponse"]] = []

    class Config:
        from_attributes = True
