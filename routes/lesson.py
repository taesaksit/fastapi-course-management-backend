from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.oauth2 import get_current_user, allow_roles
from schemas import lesson as schemaLesson
from services import lesson as crud
from schemas.response import ResponseSchema
from models import user as UserModel

router = APIRouter(prefix="/lessons", tags=["lesson"])


@router.post(
    "/course/{course_id}", response_model=ResponseSchema[schemaLesson.LessonResponse]
)
def create_lesson(
    course_id: int,
    lesson: schemaLesson.LessonCreate,
    db: Session = Depends(get_db),
    current_user: UserModel.User = Depends(allow_roles("professor", "admin")),
):
    return crud.create_lesson(
        db,
        course_id,
        lesson,
        current_user,
    )


@router.put(
    "/{lesson_id}",
    response_model=ResponseSchema[schemaLesson.LessonResponse],
)
def update_lesson(
    lesson_id: int,
    lesson: schemaLesson.LessonUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel.User = Depends(allow_roles("professor", "admin")),
):
    return crud.update_lesson(db, lesson_id, lesson, current_user)
