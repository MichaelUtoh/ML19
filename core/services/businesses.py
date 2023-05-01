from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.config.permissions import has_admin_permission, has_business_permission
from core.config.utils import db_save
from core.schema.businesses import BusinessCreateSchema, LocationSchema
from core.models.accounts import User
from core.models.businesses import Business, Location


auth_handler = AuthHandler()


def locations_list_func(
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    pass


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
    user = session.query(User).where(User.email == user).first()
    if has_business_permission(user):
        return session.query(Business).where(Business.owner == user).all()
    elif has_admin_permission(user):
        return session.query(Business).all()


def business_create_func(
    data: BusinessCreateSchema,
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = session.query(User).where(User.email == user).first()
    location = session.query(Location).where(Location.id == data.location).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    business = Business(
        name=data.name,
        logo=data.logo,
        description=data.description,
        address=data.address,
        open_days=data.open_days,
        location_id=location,
        user_id=user,
    )
    return db_save(business, session)
