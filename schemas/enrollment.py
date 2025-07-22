from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from schemas.course import CourseResponse
from schemas.user import UserNameOnly


class EnrollmentBase(BaseModel):
    enrolled_at: Optional[datetime] = None


class EnrollmentCreate(BaseModel):
    course_id: int
    student_id: int


class EnrollmentResponse(EnrollmentBase):
    id: int
    course: Optional[CourseResponse] = None

    class Config:
        from_attributes = True


class StudentEnrollmentInfo(BaseModel):
    id: int
    enrolled_at: datetime
    student: UserNameOnly

    class Config:
        from_attributes = True


class EnrolledCourseWithStudents(BaseModel):
    course: CourseResponse
    students: list[StudentEnrollmentInfo]
