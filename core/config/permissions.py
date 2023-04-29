from fastapi import Depends, HTTPException

from core.models.accounts import UserStatus


def has_admin_permission(user):
    if not user.status == UserStatus.ADMIN:
        msg = 'Access denied, Kindly contact Admin'
        raise HTTPException(status_code=404, detail=msg)


def has_business_permission(user):
    if not user.status == UserStatus.BUSINESS_OWNER:
        msg = 'Access denied, Kindly contact Admin'
        raise HTTPException(status_code=404, detail=msg)


def has_customer_permission(user):
    if not user.status == UserStatus.CUSTOMER:
        msg = 'Access denied, Kindly contact Admin'
        raise HTTPException(status_code=404, detail=msg)
