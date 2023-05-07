from typing import Optional

from cloudinary.uploader import upload
from decouple import config
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.config.permissions import has_admin_permission, has_business_permission
from core.config.utils import db_save, db_bulk_delete, db_obj_by_uuid
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
    business.name = data.name
    business.description = data.description
    business.open_days = data.open_days
    business.address = data.address
    business.location_id = data.location

    business = db_save(business, session)

    business.open_days = business.open_days.strip("{}").split(",")
    business.location = (
        session.query(Location).where(Location.id == business.location_id).first()
    )
    return business


def business_logo_func(uuid, file, user, session):
    business = db_obj_by_uuid(uuid, Business, session)
    folder_path = f"businesses/{business.name}{business.uuid[:7]}"
    res = upload(file.file, folder=folder_path)
    logo_url = res["secure_url"]
    business.logo = logo_url
    data = db_save(business, session)
    business.open_days = business.open_days.strip("{}").split(",")
    business.location = (
        session.query(Location).where(Location.id == business.location_id).first()
    )
    return data


def business_delete_func(
    ids: list,
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = session.query(User).where(User.email == user).first()
    if not has_admin_permission(user):
        raise HTTPException(status_code=404, detail="Not allowed, Kindly contact Admin")

    db_bulk_delete(ids, Business, session)
