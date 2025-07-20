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
        db_course = (
            db.query(CourseModel)
            .filter(CourseModel.professor_id == current_user.id)
            .all()
        )
        if not db_course:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You do not have any courses",
            )

    except SQLAlchemyError as e:
        # ดักจับ error จาก DB
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error: " + str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error: " + str(e),
        )

    return ResponseSchema(
        status="success", message="List of all your course", data=db_course
    )


# Path: /me/courses/enrolled
# get_enrolled_courses
