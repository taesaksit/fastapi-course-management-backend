from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models import user as UserModel
from models.lesson import Lesson as LessonModel
from models.course import Course as CourseModel
from schemas import lesson as schemaLesson
from schemas.response import ResponseSchema


def create_lesson(
    db: Session,
    course_id: int,
    lesson: schemaLesson.LessonCreate,
    current_user: UserModel.User,
):

    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if db_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if db_course.professor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to add lesson to this course",
        )

    max_order = (
        db.query(LessonModel.order)
        .filter(LessonModel.course_id == course_id)
        .order_by(LessonModel.order.desc())
        .first()
    )
    if max_order:
        next_order = max_order[0] + 1
    else:
        next_order = 1

    new_lesson = LessonModel(
        **lesson.model_dump(),
        course_id=course_id,
        order=next_order,
    )

    try:
        db.add(new_lesson)
        db.commit()
        db.refresh(new_lesson)

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

    return ResponseSchema(
        status="success",
        message="Lesson created successfully",
        data=new_lesson,
    )
