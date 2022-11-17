from typing import Type

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from dependencies import db
from internal.authentication import users
from internal.models import User

router = APIRouter()


@router.post("/register", tags=["register"], response_model=User)
def register(
    username: str,
    password: str,
    password2: str,
    session: Session = Depends(db.get_session),
) -> Type[User] | HTTPException:
    if password != password2:
        raise HTTPException(status_code=422, detail="Passwords do not match")
    user = users.register(username, password, session)
    if not user:
        raise HTTPException(status_code=422, detail="Username already in use")
    return user
