import csv
import datetime
from typing import Optional

from cloudinary.uploader import upload
from decouple import config
from fastapi import Depends, HTTPException
from fastapi_pagination import paginate
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.config.permissions import (
    has_admin_permission,
    has_customer_permission,
    has_business_permission,
)
from core.config.utils import (
    business_location_func,
    db_queryset,
    db_obj_by_id,
    db_obj_by_uuid,
    db_obj_delete,
    db_save,
    get_db_user,
    get_qs_by_fkeys,
)
from core.schema.businesses import BusinessCreateSchema, LocationSchema
from core.models.accounts import User
from core.models.businesses import Business, Location, Product, Review


auth_handler = AuthHandler()


def locations_list_func(
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    # TODO Requires permission???
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
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = get_db_user(user, session)
    business_qs = db_queryset(Business, session)

    user_businesses = []
    for idx in business_qs:
        if has_business_permission(user, idx):
            user_businesses.append(idx)

    if user_businesses:
        business_location_func(user_businesses, session)
        return paginate(user_businesses)
    elif has_admin_permission(user):
        business_location_func(business_qs, session)
        return paginate(business_qs)


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

    obj = Business(
        name=data.name,
        description=data.description,
        address=data.address,
        open_days=data.open_days,
        location_id=location.id,
        user_id=user.id,
    )
    business = db_save(obj, session)
    business_location_func([business], session)
    return business


def business_obj_func(
    uuid: str,
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = get_db_user(user, session)
    business = db_obj_by_uuid(uuid, Business, session)

    if not has_admin_permission(user) and not has_business_permission(user, business):
        raise HTTPException(status_code=404, detail="Not Allowed, Kindly contact Admin")

    business_location_func([business], session)
    return business


def business_update_func(
    uuid: str,
    data: BusinessCreateSchema,
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = session.query(User).where(User.email == user).first()
    business = db_obj_by_uuid(uuid, Business, session)
    if not has_admin_permission(user) and not has_business_permission(user, business):
        raise HTTPException(status_code=404, detail="Not Allowed, Kindly contact Admin")

    business.name = data.name
    business.description = data.description
    business.open_days = data.open_days
    business.address = data.address
    business.location_id = data.location
    business = db_save(business, session)
    business_location_func([business], session)
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
    uuid: str,
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    business = db_obj_by_uuid(uuid, Business, session)
    user = db_obj_by_id(user, User, session)
    if not has_business_permission(user, business):
        raise HTTPException(status_code=404, detail="Not allowed, Kindly contact Admin")
    db_obj_delete(business, session)


def get_business_products_func(uuid, user, session):
    try:
        user = get_db_user(user, session)
        business = db_obj_by_uuid(uuid, Business, session)
    except:
        msg = "Something went wrong, Kindly contact admin"
        raise HTTPException(status_code=404, detail=msg)

    if not has_admin_permission(user) and not has_business_permission(user, business):
        raise HTTPException(status_code=404, detail="Not allowed, Kindly contact Admin")

    business.products = get_qs_by_fkeys(business, Product, session)
    data = paginate(business.products) if len(business.products) > 0 else []
    return data


def add_business_products_func(uuid, data, user, session):
    try:
        user = get_db_user(user, session)
        business = db_obj_by_uuid(uuid, Business, session)
    except:
        raise HTTPException(status_code=404, detail="Not found")

    if not has_business_permission(user, business):
        raise HTTPException(status_code=404, detail="Not allowed, Kindly contact Admin")

    obj = Product(
        name=data.name,
        product_no=data.product_no,
        description=data.description,
        business_id=business.id,
    )
    return db_save(obj, session)


def batch_upload_func(uuid, user, file, session):
    try:
        user = get_db_user(user, session)
        business = db_obj_by_uuid(uuid, Business, session)
    except:
        msg = "Something went wrong, Kindly contact admin"
        raise HTTPException(status_code=404, detail=msg)

    if not has_business_permission(user, business):
        msg = "Not allowed"
        raise HTTPException(status_code=404, detail=msg)

    if not file.filename.endswith(".csv"):
        msg = "Only files with '.csv' type are allowed"
        raise HTTPException(status_code=404, detail=msg)

    count = 0
    content = file.file.read().decode("utf-8")
    csv_data = csv.DictReader(content.splitlines())

    batch = []
    for row in csv_data:
        new = Product(
            name=row["NAME"],
            product_no=row["PRODUCT NUMBER"],
            description=row.get("DESCRIPTION"),
            business_id=business.id,
            created_timestamp=datetime.datetime.now(),
        )
        batch.append(new)
        count += 1

    for obj in batch:
        db_save(obj, session)

    return {"detail": f"{count} products uploaded successfully"}


def get_business_review_func(uuid, user, session):
    try:
        user = get_db_user(user, session)
        business = db_obj_by_uuid(uuid, Business, session)
    except:
        msg = "Something went wrong, Kindly contact admin"
        raise HTTPException(status_code=404, detail=msg)

    if not has_business_permission(user, business):
        msg = "Not allowed"
        raise HTTPException(status_code=404, detail=msg)

    business.reviews = get_qs_by_fkeys(business, Review, session)
    data = paginate(business.reviews) if len(business.reviews) > 0 else []
    return data


def add_business_review_func(uuid, data, user, session):
    try:
        user = get_db_user(user, session)
        business = db_obj_by_uuid(uuid, Business, session)
    except:
        raise HTTPException(status_code=404, detail="Not found")

    if not has_customer_permission(user):
        raise HTTPException(status_code=404, detail="Not allowed, Kindly contact Admin")

    review = Review(user_id=user.id, business_id=business.id, description=data.description)
    return db_save(review, session)