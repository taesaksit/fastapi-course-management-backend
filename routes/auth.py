from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from services import auth as crud
from core.oauth2 import allow_roles

from models.user import User
from schemas import user as schemasUser
from schemas.response import ResponseSchema

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=ResponseSchema[schemasUser.UserResponse], tags=["auth"])
def register(user: schemasUser.RegisterCreate, db: Session = Depends(get_db)):
    return crud.register(db, user)


@router.post("/login", response_model=ResponseSchema[schemasUser.LoginResponse], tags=["auth"])
def login(user: schemasUser.LoginCreate, db: Session = Depends(get_db)):
    return crud.login(db, user)


