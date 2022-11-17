from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from dependencies import db
from internal.authentication import users
from internal.crud import crud
from store.models import Category

router = APIRouter(dependencies=[Depends(users.get_current_username)])


@router.get("/categories", tags=["categories"], response_model=list[Category])
def categories(session: Session = Depends(db.get_session)) -> list[Category]:
    objects = crud.get_objects(session, Category)
    return objects


@router.get("/categories/{id}", tags=["categories"], response_model=Category)
def category(id: int, session: Session = Depends(db.get_session)) -> Category | HTTPException:
    object = crud.get_object(session, Category, id=id)
    if not object:
        raise HTTPException(status_code=404, detail="Not Found")
    return object
