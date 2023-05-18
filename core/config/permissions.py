from fastapi import Depends, HTTPException

from core.models.accounts import UserStatus


def has_admin_permission(user):
    if not user.status == UserStatus.ADMIN:
        return False
    return True


def has_business_permission(user, business):
    if not business.user.email == user.email:
        return False
    return True


def has_customer_permission(user):
    if not user.status == UserStatus.CUSTOMER:
        return False
    return True


def has_owner_permission(user, business):
    if not business.owner == user:
        return False
    return True
