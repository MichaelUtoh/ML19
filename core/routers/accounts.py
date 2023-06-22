from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SQA_Session

from core.services.accounts import (
    _delete_user_func,
    _get_user_info_func,
    _list_users_func,
    _login_func,
    _signup_func,
    _update_func,
    _user_profile_schema,
)

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.schema.accounts import (
    AuthPassSchema,
    ProfileCreateSchema,
    UserCreateBasicSchema,
    UserDetailSchema,
    UserUpdateSchema,
)


router = APIRouter(prefix="/auth", tags=["Auth"])

auth_handler = AuthHandler()


@router.post("/login", status_code=200)
def login(data: UserCreateBasicSchema, session: SQA_Session = Depends(get_session)):
    data = _login_func(data, session)
    return data


@router.post("/register", status_code=200)
def register(data: UserCreateBasicSchema, session: SQA_Session = Depends(get_session)):
    data = _signup_func(data, session)
    return data


@router.get("/users/me", response_model=UserDetailSchema, status_code=200)
def get_user_profile(
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    res = _get_user_info_func(user, session)
    return res


# @router.get("/users/all", response_model=List[UserDetailSchema], status_code=200)
# def all_users(
#     user=Depends(auth_handler.auth_wrapper),
#     session: SQA_Session = Depends(get_session),
#     search: str | None = None,
# ):
#     # TODO Verify user status on db
#     res = list_users_func(user, session, search=search)
#     return res


@router.put("/users/{id}/update", response_model=UserDetailSchema)
def update_user(
    id: int,
    data: UserUpdateSchema,
    email=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    res = _update_func(id, email, data, session)
    return res


@router.post("/users/{id}/profile/add", response_model=None)
def add_user_profile(
    id: int,
    data: ProfileCreateSchema,
    email=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    res = _user_profile_schema(id, email, data, session)
    return res


# # Change logic to archive
# @router.delete("/users/{id}/delete", status_code=204)
# def terminate_account(
#     id: int,
#     user=Depends(auth_handler.auth_wrapper),
#     session: SQA_Session = Depends(get_session),
# ):
#     delete_user_func(id, user, session)
#     return
