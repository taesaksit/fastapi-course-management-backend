from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

from models.course import Course as CourseModel
from models import user as UserModel
from models.enrollment import Enrollment as EnrollmentModel
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


def get_enrolled_courses(db: Session, current_user: UserModel.User):
    try:
        enrollments = (
            db.query(EnrollmentModel)
            .filter(EnrollmentModel.student_id == current_user.id)
            .join(CourseModel)
            .all()
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

    if not enrollments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You have not enrolled in any courses",
        )

    # ดึงเฉพาะคอร์สออกมา
    enrolled_courses = [enroll.course for enroll in enrollments]
    
    return ResponseSchema(
        status="success",
        message="List of enrolled courses",
        data=enrolled_courses,
    )