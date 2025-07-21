from fastapi import HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.course import Course as CourseModel
from models.user import User as UserModel
from models.lesson import Lesson as LessonModel

from schemas import course as schemasCourse
from schemas.response import ResponseSchema


def create_course(
    db: Session,
    course: schemasCourse.CourseCreate,
    current_user: UserModel,
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


def get_course_by_id(db: Session, courese_id: int) -> ResponseSchema:
    try:
        db_course = db.query(CourseModel).filter(CourseModel.id == courese_id).first()

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


def get_lessons(db: Session, course_id: int) -> ResponseSchema:

    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

    if db_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    try:
        db_lessons = (
            db.query(LessonModel).filter(LessonModel.course_id == course_id).all()
        )

        if not db_lessons:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No lessons found in this course",
            )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

    return ResponseSchema(
        status="success",
        message="Lessons found",
        data={
            "course_title": db_course.title,
            "lessons": db_lessons,
        },
    )


def update_course(
    db: Session,
    course_id: int,
    course: schemasCourse.CourseCreate,
    current_user: UserModel,
) -> ResponseSchema:

    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

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


def delete_coruse(db: Session, course_id: int, current_user: UserModel):

    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

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
