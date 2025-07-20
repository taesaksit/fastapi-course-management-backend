from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.oauth2 import allow_roles


from crud import course as crud
from models import user as UserModel
from schemas import course as schemasCourse
from schemas.response import ResponseSchema

router = APIRouter(prefix="/course")


@router.post("/", response_model=ResponseSchema[schemasCourse.CourseResponse])
def create_course(
    course: schemasCourse.CourseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(allow_roles("professor", "admin")),
):
    return crud.create_course(db, course,current_user)
