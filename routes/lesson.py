from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.oauth2 import get_current_user, allow_roles
from schemas import lesson as schemasLesson
from services import lesson as crud
from schemas.response import ResponseSchema
from models import user as UserModel

router = APIRouter(prefix="/lessons", tags=["lesson"])


@router.post(
    "/course/{course_id}", response_model=ResponseSchema[schemasLesson.LessonResponse]
)
def create_lesson(
    course_id: int,
    lesson: schemasLesson.LessonCreate,
    db: Session = Depends(get_db),
    current_user: UserModel.User = Depends(allow_roles("professor", "admin")),
):
    return crud.create_lesson(
        db,
        course_id,
        lesson,
        current_user,
    )
