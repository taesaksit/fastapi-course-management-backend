from fastapi import HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.exception_handlers import handle_general_exception, handle_sqlalchemy_error

from models.course import Course as CourseModel
from models import user as UserModel

from schemas import course as schemasCourse
from schemas.response import ResponseSchema


def create_course(
    db: Session,
    course: schemasCourse.CourseCreate,
    current_user: UserModel.User,
) -> ResponseSchema:

    course_data = course.model_dump()
    course_data["professor_id"] = current_user.id
    new_course = CourseModel(**course_data)

    try:
        db.add(new_course)
        db.commit()
        db.refresh(new_course)

        return ResponseSchema(
            status="success",
            message="Create course successfully",
            data=new_course,
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )


def get_courses(db: Session, keyword: Optional[str]) -> ResponseSchema:
    query = db.query(CourseModel)

    if keyword:
        query = query.filter(CourseModel.title.ilike(f"%{keyword}%"))

    query = query.order_by(CourseModel.id)

    try:
        results = query.all()

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course Not found",
        )

    return ResponseSchema(
        status="success",
        message="List of all courses",
        data=results,
    )


def get_course_by_id(db: Session, id: int) -> ResponseSchema:
    try:
        db_course = db.query(CourseModel).filter(CourseModel.id == id).first()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

    if db_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    return ResponseSchema(
        status="success",
        message="Course by id result",
        data=db_course,
    )


def update_course(
    db: Session,
    id_course: int,
    course: schemasCourse.CourseCreate,
    current_user: UserModel.User,
) -> ResponseSchema:

    db_course = db.query(CourseModel).filter(CourseModel.id == id_course).first()

    if db_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if db_course.professor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this course",
        )

    update_data = course.model_dump()

    try:
        for key, value in update_data.items():
            setattr(db_course, key, value)

        db.commit()
        db.refresh(db_course)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

    return ResponseSchema(
        status="success",
        message="Course update successfully",
        data=db_course,
    )


def delete_coruse(db: Session, id_course: int, current_user: UserModel.User):

    db_course = db.query(CourseModel).filter(CourseModel.id == id_course).first()

    if db_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if db_course.professor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this course",
        )

    course_name = db_course.title

    try:
        db.delete(db_course)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )
    return ResponseSchema(
        status="success",
        message=f"Delete course {course_name} ",
    )
