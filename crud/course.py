from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

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


def get_courses(db: Session, keyword: Optional[str]):

    query = db.query(
        CourseModel
    )  # สร้าง Query Object จากตาราง CourseModel ยังไม่ดึงข้อมูลจากฐานข้อมูล

    if keyword:
        query = query.filter(CourseModel.title.ilike(f"%{keyword}%"))

    results = query.all()  # ยิง SQL query ไปที่ฐานข้อมูล

    if not results:
        raise HTTPException(status_code=404, detail="No matching courses found")
    return ResponseSchema(status="success", message="List of all courses", data=results)


def get_course_by_id(db: Session, id: int):
    try:
        db_course = db.query(CourseModel).filter(CourseModel.id == id).first()

        if db_course is None:
            raise ValueError("Course not found")
        return ResponseSchema(
            status="success", message="Course by id result", data=db_course
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
