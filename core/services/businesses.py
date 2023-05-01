from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.config.permissions import has_admin_permission, has_business_permission
from core.schema.businesses import BusinessCreateSchema
from core.models.accounts import User
from core.models.businesses import Business


auth_handler = AuthHandler()


def location_create_func(
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    pass


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
    business = Business(
        name=data.name,
        logo=data.logo,
        description=data.description,
        address=data.address,
    )
    session.add(User)
    return
