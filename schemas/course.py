from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas.user import UserNameOnly


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    professor: Optional[UserNameOnly] = None

    class Config:
        from_attributes = True
