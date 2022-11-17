from typing import Type

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session

import dependencies
from dependencies import db
from internal.crud import crud
from internal.models import User

security = HTTPBasic()


class Users:
    @classmethod
    def authenticate_user(cls, session, username: str, password: str) -> Type[User] | bool:  # type: ignore
        user = crud.get_object(session, User, username=username)
        if not user:
            return False
        if not cls.verify_password(password, user.hashed_password):
            return False
        return user

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:  # type: ignore
        return dependencies.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:  # type: ignore
        return dependencies.pwd_context.hash(password)

    @classmethod
    def get_current_username(
        cls,
        credentials: HTTPBasicCredentials = Depends(security),
        session: Session = Depends(db.get_session),
    ) -> Type[User] | HTTPException:
        user = crud.get_object(session, User, username=credentials.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username not found")
        if not cls.verify_password(credentials.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        return user

    @classmethod
    def register(cls, username: str, password: str, session: Session) -> Type[User] | None:
        hashed_password = cls.get_password_hash(password)
        try:
            user = crud.create_object(session, User, username=username, hashed_password=hashed_password)
            return user
        except Exception:
            return None


users = Users()
