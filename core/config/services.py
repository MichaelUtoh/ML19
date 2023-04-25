from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from decouple import config
from zxcvbn import zxcvbn

from fastapi import Depends, HTTPException, Security
from sqlmodel import Session, select

from core.models.accounts import User
from core.config.auth import AuthHandler


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


def list_users_func(session):
    with session:
        return session.exec(select(User)).all()


def signup_func(data, session):
    if session.exec(select(User).where(User.email == data.email)).first():
        msg = "User with the given email already exists"
        raise HTTPException(status_code=400, detail=msg)

    if not pwd_strength_checker(data):
        return {"detail": "Password is not strong enough!"}

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(data.password.encode("utf-8"), salt)

    user = User(email=data.email.lower(), password=hashed_pwd)
    session.add(user)
    session.commit()
    session.refresh(user)

    payload = {
        "email": user.email,
        "uuid": user.uuid,
        "access_token": auth_handler.encode_token(user.email),
        "refresh_token": auth_handler.encode_refresh_token(user.email),
    }
    return payload


def login_func(data, session):
    statement = select(User).where(User.email == data.email.lower())
    res = session.exec(statement)
    user = res.first()

    if not auth_handler.verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    payload = {
        "email": user.email,
        "uuid": user.uuid,
        "access_token": auth_handler.encode_token(user.email),
        "refresh_token": auth_handler.encode_refresh_token(user.email),
    }
    return payload


def update_func(id, data, session):
    with session:
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
        user.phone = data.phone
        user.address1 = data.address1
        user.address2 = data.address2
        user.next_of_kin_first_name = data.next_of_kin_first_name
        user.next_of_kin_last_name = data.next_of_kin_last_name
        user.next_of_kin_phone = data.next_of_kin_phone
        user.next_of_kin_address = data.next_of_kin_address
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def delete_user_func(id, session):
    statement = select(User).where(User.id == id)
    res = session.exec(statement)
    user = res.first()
    session.delete(user)
    session.commit()
    return
