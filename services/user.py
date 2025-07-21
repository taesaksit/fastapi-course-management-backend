from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

from models.course import Course as CourseModel
from models import user as UserModel

from schemas import course as schemasCourse
from schemas.response import ResponseSchema


def get_owned_courses(db: Session, current_user: UserModel.User):
    try:
        db_courses = (
            db.query(CourseModel)
            .filter(CourseModel.professor_id == current_user.id)
            .all()
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

    if not db_courses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You do not have any courses",
        )

    return ResponseSchema(
        status="success",
        message="List of all your courses",
        data=db_courses,
    )


# Path: /me/courses/enrolled
# get_enrolled_courses
