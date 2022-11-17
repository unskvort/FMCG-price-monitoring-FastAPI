from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from dependencies import db
from internal.authentication import users
from internal.crud import crud
from store.models import Product

router = APIRouter(dependencies=[Depends(users.get_current_username)])


@router.get("/products", tags=["products"], response_model=list[Product])
def products(session: Session = Depends(db.get_session)) -> list[Product]:
    objects = crud.get_objects(session, Product)
    return objects


@router.get("/products/{id}", tags=["products"], response_model=Product)
def product(id: int, session: Session = Depends(db.get_session)) -> Product | HTTPException:
    object = crud.get_object(session, Product, id=id)
    if not object:
        raise HTTPException(status_code=404, detail="Not Found")
    return object
