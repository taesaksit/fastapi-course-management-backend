from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.security import hash_password, verify_password, create_access_token


from models.user import User as UserModel
from schemas import user as schemasUser
from schemas.response import ResponseSchema


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


# Register
def register(db: Session, user: schemasUser.RegisterCreate) -> ResponseSchema:

    try:
        existing_user = get_user_by_email(db, user.email)
        if existing_user:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        new_user = UserModel(
            email=user.email,
            name=user.name,
            password=hash_password(user.password),
            role=user.role,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return ResponseSchema(
            status="success",
            message="Register successfully",
            data=new_user,
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unexpected error: {e}"
        )


# Login
def login(db: Session, user: schemasUser.LoginCreate):
    try:
        db_user = get_user_by_email(db, user.email)
        if not db_user or not verify_password(user.password, db_user.password):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="email or password incorrect",
            )

        payload = {
            "sub": db_user.email,
            "id": db_user.id,
            "name": db_user.name,
        }
        token = create_access_token(data=payload)

        return ResponseSchema(
            status="success",
            message="Login successfully",
            data={"access_token": token, "token_type": "Bearer"},
        )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}",
        )
