from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None


class LessonCreate(LessonBase):
    pass


class LessonResponse(LessonBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class LessonResponseWithCourseName(BaseModel):
    course_title: str
    lessons: List[LessonResponse]
