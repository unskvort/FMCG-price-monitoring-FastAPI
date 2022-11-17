from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from dependencies import db
from internal.authentication import users
from internal.crud import crud
from store.models import PriceRecord

router = APIRouter(dependencies=[Depends(users.get_current_username)])


@router.get("/prices", tags=["prices"], response_model=list[PriceRecord])
def prices(session: Session = Depends(db.get_session)) -> list[PriceRecord]:
    objects = crud.get_objects(session, PriceRecord)
    return objects


@router.get("/prices/{id}", tags=["prices"], response_model=list[PriceRecord])
def price(id: int, session: Session = Depends(db.get_session)) -> list[PriceRecord] | HTTPException:
    object = crud.get_object(session, PriceRecord, product=id, many=True)
    if not object:
        raise HTTPException(status_code=404, detail="Not Found")
    return object
