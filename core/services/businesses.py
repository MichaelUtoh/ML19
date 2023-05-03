from typing import Optional

from decouple import config
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.config.permissions import has_admin_permission, has_business_permission
from core.config.utils import db_save, db_bulk_delete
from core.schema.businesses import BusinessCreateSchema, LocationSchema
from core.models.accounts import User
from core.models.businesses import Business, Location


auth_handler = AuthHandler()


def locations_list_func(
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = session.query(User).where(User.email == user).first()
    if not has_business_permission(user) and not has_admin_permission(user):
        raise HTTPException(status_code=404, detail="Not allowed, Kindly contact admin")
    return session.query(Location).all()


def locations_create_func(
    data: LocationSchema,
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = session.query(User).where(User.email == user).first()
    if not has_admin_permission(user):
        raise HTTPException(status_code=404, detail="Not allowed, Kindly contact admin")

    location = Location(state=data.state, capital=data.capital)
    return db_save(location, session)


def business_list_func(
    uuid: Optional[str],
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = []
    user = session.query(User).where(User.email == user).first()
    if has_business_permission(user):
        data = session.query(Business).where(Business.user == user).all()
        for idx in data:
            idx.open_days = idx.open_days.strip("{}").split(",")
            idx.location = (
                session.query(Location).where(Location.id == idx.location_id).first()
            )

    elif has_admin_permission(user):
        data = session.query(Business).all()
        for idx in data:
            idx.open_days = idx.open_days.strip("{}").split(",")
            idx.location = (
                session.query(Location).where(Location.id == idx.location_id).first()
            )

    return data


def business_create_func(
    data: BusinessCreateSchema,
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = session.query(User).where(User.email == user).first()
    if len(user.businesses) == config("BUSINESS_COUNT_MAX"):
        msg = "You have reached maximum number of businesses allowed"
        raise HTTPException(status_code=404, detail=msg)
    location = session.query(Location).where(Location.id == data.location).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    business = Business(
        name=data.name,
        logo=data.logo,
        description=data.description,
        address=data.address,
        open_days=data.open_days,
        location_id=location.id,
        user_id=user.id,
    )
    # print('=================>')
    # print(business)
    # print('<=================')
    return db_save(business, session)




def business_update_func(
        uuid: str,
    data: BusinessCreateSchema,
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = session.query(User).where(User.email == user).first()
    if not has_admin_permission(user) and not has_business_permission(user):
        raise HTTPException(status_code=404, detail="Not Allowed, Kindly contact Admin")

    business = session.query(Business).where(Business.uuid == uuid).first()
    if not business:
        raise HTTPException(status_code=404, detail="Not found")
    
    print(data.dict())




def business_delete_func(
    ids: list,
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = session.query(User).where(User.email == user).first()
    if not has_admin_permission(user):
        raise HTTPException(status_code=404, detail="Not allowed, Kindly contact Admin")

    db_bulk_delete(ids, Business, session)
