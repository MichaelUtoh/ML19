from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.config.permissions import has_admin_permission, has_business_permission
from core.models.accounts import User
from core.models.businesses import Business


auth_handler = AuthHandler()


def business_list_func(
    uuid: Optional[str],
    user: Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    user = session.query(User).where(User.email == user).first()
    business_list = None
    
    try:
        has_admin_permission(user)
        business_list = session.query(Business).all()
    except:
        business_list = session.query(Business).where(Business.owner == user).all()
        pass
