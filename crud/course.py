from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.course import Course as CourseModel
from models import user as UserModel

from schemas import course as schemasCourse
from schemas.response import ResponseSchema


def create_course(
    db: Session, course: schemasCourse.CourseCreate, current_user: UserModel.User
):
    try:

        course_data = course.model_dump()
        course_data["professor_id"] = current_user.id
        new_course = CourseModel(**course_data)

        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return ResponseSchema(
            status="success", message="Create course successfully", data=new_course
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error: " + str(e))


def view_course(db: Session):
    all_course = db.query(CourseModel).all()

    return ResponseSchema(status="success", message="List All courses", data=all_course)
