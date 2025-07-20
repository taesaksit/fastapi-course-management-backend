from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import user as crud
from core.oauth2 import allow_roles
from typing import List

from models import user as UserModel
from schemas import user as schemasUser
from schemas import course as schemasCourse
from schemas.response import ResponseSchema

router = APIRouter(prefix="/user")


@router.get("/me", response_model=ResponseSchema[schemasUser.UserResponse])
def get_current_user_profile(
    current_user: UserModel = Depends(allow_roles("admin", "professor", "student"))
):
    return ResponseSchema(status="success", message="My profile", data=current_user)


# READ my course from professor
@router.get(
    "/me/courses/owned",
    response_model=ResponseSchema[List[schemasCourse.CourseResponse]],
)
def get_owned_courses(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(allow_roles("professor")),
):
    return crud.get_owned_courses(db, current_user)
