from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from core.oauth2 import allow_roles
from schemas import enrollment as schemaEnrollment
from services import enrollment as crud
from schemas.response import ResponseSchema
from models import user as UserModel

router = APIRouter(prefix="/enrollment", tags=["enrollment"])


@router.post(
    "/",
    response_model=ResponseSchema[schemaEnrollment.EnrollmentResponse],
    tags=["enrollment"],
)
def enrollment_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel.User = Depends(allow_roles("student")),
):
    return crud.enrollment_course(
        db,
        course_id,
        current_user,
    )


@router.get(
    "/{course_id}/students",
    response_model=ResponseSchema[schemaEnrollment.EnrolledCourseWithStudents],
    tags=["enrollment"],
)
def get_students_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel.User = Depends(allow_roles("professor")),
):
    return crud.get_students_in_course(course_id, db, current_user)
