from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from core.oauth2 import allow_roles
from typing import List, Optional


from services import course as crud
from models import user as UserModel
from schemas import course as schemasCourse
from schemas import lesson as schemasLesson
from schemas.response import ResponseSchema

router = APIRouter(prefix="/course")


# CREATE
@router.post(
    "/", response_model=ResponseSchema[schemasCourse.CourseResponse], tags=["course"]
)
def create_course(
    course: schemasCourse.CourseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(allow_roles("professor", "admin")),
):
    return crud.create_course(db, course, current_user)


# READ OR SEARCH
@router.get(
    "/",
    response_model=ResponseSchema[List[schemasCourse.CourseResponse]],
    tags=["course"],
)
def get_courses(keyword: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return crud.get_courses(db, keyword)


# READ BY ID
@router.get(
    "/{course_id}",
    response_model=ResponseSchema[schemasCourse.CourseResponse],
    tags=["course"],
)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    return crud.get_course_by_id(db, course_id)


# READ Lesson
@router.get(
    "/{course_id}/lesson",
    response_model=ResponseSchema[schemasLesson.LessonResponseWithCourseName],
    tags=["course"],
)

def get_lessons(course_id: int, db: Session = Depends(get_db)):
    return crud.get_lessons(db, course_id)


# Update
@router.put(
    "/{course_id}",
    response_model=ResponseSchema[schemasCourse.CourseResponse],
    tags=["course"],
)
def update_course(
    course_id: int,
    course: schemasCourse.CourseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(allow_roles("professor", "admin")),
):
    return crud.update_course(db, course_id, course, current_user)


# Delete
@router.delete("/{course_id}", tags=["course"])
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(allow_roles("professor", "admin")),
):
    return crud.delete_coruse(db, course_id, current_user)
