from pydantic import BaseModel
from typing import Optional 
from datetime import datetime

from course import CourseResponse
from user import UserResponse

class EnrollmentBase(BaseModel):
    enrolled_at: Optional[datetime] = None

class EnrollmentCreate(BaseModel):
    course_id: int
    student_id: int

class EnrollmentResponse(EnrollmentBase):
    id: int
    course: Optional[CourseResponse] = None
    student: Optional[UserResponse] = None

    class Config:
        from_attributes = True
