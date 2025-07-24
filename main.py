from models import user, course, lesson
from fastapi import FastAPI, HTTPException
from config.database import Base, engine
from core.exception_handlers import http_exception_handler
from routes import auth, course, user, lesson, enrollment

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(auth.router, prefix="/api")
app.include_router(course.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(lesson.router, prefix="/api")
app.include_router(enrollment.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Course Management!"}
