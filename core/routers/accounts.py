from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SQA_Session

from core.config.services import (
    get_user_info_func,
    list_users_func,
    login_func,
    signup_func,
    update_func,
)

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.schema.accounts import (
    AuthPassSchema,
    UserCreateBasicSchema,
    UserDetailSchema,
    UserUpdateSchema,
)


router = APIRouter(prefix="/auth", tags=["Auth"])

auth_handler = AuthHandler()


@router.post("/login", status_code=200)
def login(data: UserCreateBasicSchema, session: SQA_Session = Depends(get_session)):
    data = login_func(data, session)
    return data


@router.post("/register", status_code=200)
def register(data: UserCreateBasicSchema, session: SQA_Session = Depends(get_session)):
    data = signup_func(data, session)
    return data


@router.get("/users/me", response_model=UserDetailSchema, status_code=200)
def all_users(
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    res = get_user_info_func(user, session)
    return res


@router.get("/users/all", response_model=List[UserDetailSchema], status_code=200)
def all_users(
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
    search: str | None = None,
):
    # TODO Verify user status on db
    res = list_users_func(user, session, search=search)
    return res


@router.put("/users/{id}/update", response_model=UserDetailSchema)
def update_user(
    id: int,
    data: UserUpdateSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    res = update_func(id, user, data, session)
    return res
