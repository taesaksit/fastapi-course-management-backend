from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from models.user import User as UserModel
from models.enrollment import Enrollment as EnrollmentModel
from models.course import Course as CourseModel

# from schemas import enrollment as schemaEnrollment
from schemas.response import ResponseSchema


def enrollment_course(db: Session, course_id: int, current_user: UserModel):
    # 1. ตรวจสอบว่าคอร์สมีอยู่จริงหรือไม่
    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    # 2. ตรวจสอบว่าผู้ใช้ลงทะเบียนคอร์สนี้ไปแล้วหรือยัง
    already_enrolled = (
        db.query(EnrollmentModel)
        .filter_by(
            course_id=course_id,
            student_id=current_user.id,
        )
        .first()
    )

    if already_enrolled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already enrolled in this course",
        )

    # 3. สร้าง Enrollment ใหม่
    new_enrollment = EnrollmentModel(
        course_id=course_id,
        student_id=current_user.id,
    )

    # 4. บันทึกข้อมูลลงฐานข้อมูล
    try:
        db.add(new_enrollment)
        db.commit()
        db.refresh(new_enrollment)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )

    # 5. ส่ง response กลับ
    return ResponseSchema(
        status="success",
        message="Enrollment successful",
        data=new_enrollment,
    )


def get_students_in_course(course_id: int, db: Session, current_user: UserModel):
    try:

        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found",
            )

        if course.professor_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

        enrollments = (
            db.query(EnrollmentModel)
            .options(joinedload(EnrollmentModel.student))
            .filter(EnrollmentModel.course_id == course_id)
            .all()
        )

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return ResponseSchema(
        status="success",
        message="List of students enrolled in this course",
        data={
            "course": course,
            "students": enrollments,
        },
    )
