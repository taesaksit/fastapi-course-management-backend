from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import auth as crud
from core.oauth2 import allow_roles

from models.user import User
from schemas import user as schemasUser
from schemas.response import ResponseSchema

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=ResponseSchema[schemasUser.UserResponse])
def register(user: schemasUser.RegisterCreate, db: Session = Depends(get_db)):
    return crud.register(db, user)


@router.post("/login", response_model=ResponseSchema[schemasUser.LoginResponse])
def login(user: schemasUser.LoginCreate, db: Session = Depends(get_db)):
    return crud.login(db, user)


