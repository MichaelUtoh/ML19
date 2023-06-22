from datetime import datetime, timedelta

import bcrypt
import jwt
from decouple import config
from zxcvbn import zxcvbn

from fastapi import HTTPException
from sqlmodel import select

from core.models.accounts import Profile, User, UserStatus
from core.models.businesses import Business, Location
from core.config.auth import AuthHandler
from core.config.tasks import send_welcome_email_task
from core.config.utils import db_save, get_db_user, business_location_func
from core.config.permissions import (
    has_admin_permission,
    has_business_permission,
    has_customer_permission,
)


auth_handler = AuthHandler()


def pwd_strength_checker(data):
    res = zxcvbn(data.password)
    if not res["score"] >= 3:
        return False
    return True


def _get_user_info_func(email, session):
    user = get_db_user(email, session)
    return user


def _list_users_func(user, session, search=None):
    user = session.exec(select(User).where(User.email == user)).first()
    if not has_admin_permission(user):
        msg = "Access denied, Kindly contact Admin"
        raise HTTPException(status_code=404, detail=msg)
    return session.query(User).order_by(-User.id).all()


def _signup_func(data, session):
    if get_db_user(data.email, session):
        msg = "User with the given email already exists"
        raise HTTPException(status_code=400, detail=msg)

    if not pwd_strength_checker(data):
        return {"detail": "Password is not strong enough!"}

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(data.password.encode("utf-8"), salt)
    user = User(email=data.email.lower(), password=hashed_pwd)
    user = db_save(user, session)

    payload = {
        "email": user.email,
        "access_token": auth_handler.encode_token(user.email),
        "refresh_token": auth_handler.encode_refresh_token(user.email),
    }

    if config("CELERY_ENABLED"):
        email_task = send_welcome_email_task.delay()
        return payload.update({"task_id": email_task.id})

    if config("CELERY_ENABLED"):
        send_welcome_email_task.delay()

    print("No background task")
    return payload


def _login_func(data, session):
    user = get_db_user(data.email, session)
    if not user:
        msg = "Invalid credentials"
        raise HTTPException(status_code=400, detail=msg)

    if not (auth_handler.verify_password(data.password, user.password)):
        raise HTTPException(
            status_code=400, detail="Invalid password, credentials try again."
        )

    payload = {
        "email": user.email,
        "access_token": auth_handler.encode_token(user.email),
        "refresh_token": auth_handler.encode_refresh_token(user.email),
    }
    return payload


def _update_func(id, email, data, session):
    user = get_db_user(email, session)
    if not user.id == id:
        raise HTTPException(status_code=404, detail="Not allowed, kindly contact admin")

    user.username = data.username
    user.first_name = data.first_name
    user.middle_name = data.middle_name
    user.last_name = data.last_name
    user.phone = data.phone
    user.address1 = data.address1
    user.address2 = data.address2
    user.next_of_kin_first_name = data.next_of_kin_first_name
    user.next_of_kin_last_name = data.next_of_kin_last_name
    user.next_of_kin_phone = data.next_of_kin_phone
    user.next_of_kin_address = data.next_of_kin_address
    user = db_save(user, session)
    return user


def _delete_user_func(id, user, session):
    user = session.exec(select(User).where(User.email == user)).first()
    if not has_admin_permission(user):
        msg = "Access denied, Kindly contact Admin"
        raise HTTPException(status_code=404, detail=msg)

    obj = session.exec(select(User).where(User.id == id)).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found.")
    elif obj.id == user.id:
        raise HTTPException(status_code=400, detail="Not allowed.")

    session.delete(obj)
    session.commit()
    return


# Profile
def _user_profile_schema(id, email, data, session) -> Profile:
    user = get_db_user(email, session)
    if not user:
        raise HTTPException(status_code=404, detail="Not allowed, Kindly contact admin")

    profile = Profile(status=data.status, user_id=user.id)
    print(profile)
    return user
