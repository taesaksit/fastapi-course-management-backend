from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    professor = "professor"
    student = "student"


class UserBase(BaseModel):
    email: EmailStr
    name: str


class RegisterCreate(UserBase):
    password: str
    role: UserRole = UserRole.student


class LoginCreate(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True
