from datetime import datetime, timedelta

import bcrypt
import jwt
from decouple import config
from zxcvbn import zxcvbn

from fastapi import HTTPException
from sqlmodel import select

from core.models.accounts import User, UserStatus
from core.config.auth import AuthHandler
from core.config.utils import db_save, send_welcome_email_task
from core.config.permissions import (
    has_admin_permission,
    has_business_permission,
    has_customer_permission,
)


auth_handler = AuthHandler()


def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(
        minutes=config("ACCESS_TOKEN_EXPIRE_MINUTES")
    )
    data = {"sub": str(user_id), "exp": expire}
    access_token = jwt.encode(data, config("SECRET_KEY"), algorithm=config("ALGORITHM"))
    return access_token


def pwd_strength_checker(data):
    res = zxcvbn(data.password)
    if not res["score"] >= 3:
        return False
    return True


def get_user_info_func(user, session):
    with session:
        user = session.exec(select(User).where(User.email == user)).first()
        return user


def list_users_func(user, session, search=None):
    user = session.exec(select(User).where(User.email == user)).first()
    has_admin_permission(user)
    return session.query(User).order_by(-User.id).all()


def signup_func(data, session):
    if session.exec(select(User).where(User.email == data.email)).first():
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

    send_welcome_email_task()
    print("No background task")
    return payload


def login_func(data, session):
    statement = select(User).where(User.email == data.email.lower())
    res = session.exec(statement)
    user = res.first()

    if not user or not (auth_handler.verify_password(data.password, user.password)):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    payload = {
        "email": user.email,
        "access_token": auth_handler.encode_token(user.email),
        "refresh_token": auth_handler.encode_refresh_token(user.email),
    }
    return payload


def update_func(id, user, data, session):
    statement = select(User).where(User.email == user)
    user = session.exec(statement).one()

    if (not user.status == UserStatus.ADMIN) and (not user.id == id):
        raise HTTPException(status_code=404, detail="Not allowed, kindly contact admin")

    try:
        statement = select(User).where(User.id == id)
        user = session.exec(statement).one()
    except:
        msg = "User with given ID does not exist."
        raise HTTPException(status_code=404, detail=msg)

    user.username = data.username
    user.first_name = data.first_name
    user.middle_name = data.middle_name
    user.last_name = data.last_name
    user.status = data.status
    user.phone = data.phone
    user.address1 = data.address1
    user.address2 = data.address2
    user.next_of_kin_first_name = data.next_of_kin_first_name
    user.next_of_kin_last_name = data.next_of_kin_last_name
    user.next_of_kin_phone = data.next_of_kin_phone
    user.next_of_kin_address = data.next_of_kin_address
    user = db_save(user, session)
    return user


def delete_user_func(id, user, session):
    user = session.exec(select(User).where(User.email == user)).first()
    has_admin_permission(user)

    obj = session.exec(select(User).where(User.id == id)).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found.")
    elif obj.id == user.id:
        raise HTTPException(status_code=400, detail="Not allowed.")

    session.delete(obj)
    session.commit()
    return
