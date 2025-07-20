from models import user, course, lesson, enrollment
from fastapi import FastAPI, HTTPException
from database import Base, engine
from core.exception_handlers import http_exception_handler
from routes import auth, course

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(auth.router, prefix="/api")
app.include_router(course.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Course Management!"}
