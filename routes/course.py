from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from core.oauth2 import allow_roles
from typing import List, Optional


from crud import course as crud
from models import user as UserModel
from schemas import course as schemasCourse
from schemas.response import ResponseSchema

router = APIRouter(prefix="/course")


# CREATE
@router.post("/", response_model=ResponseSchema[schemasCourse.CourseResponse])
def create_course(
    course: schemasCourse.CourseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(allow_roles("professor", "admin")),
):
    return crud.create_course(db, course, current_user)


# READ OR SEARCH
@router.get("/", response_model=ResponseSchema[List[schemasCourse.CourseResponse]])
def get_courses(keyword: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return crud.get_courses(db, keyword)


# READ BY ID
@router.get("/{id}", response_model=ResponseSchema[schemasCourse.CourseResponse])
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_course_by_id(db, id)
