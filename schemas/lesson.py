from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None
    order: int

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
