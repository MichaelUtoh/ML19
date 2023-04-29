import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.config.auth import AuthHandler


auth_handler = AuthHandler()
router = APIRouter(tags=["Business"])


@router.get("/businesses")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}


@router.post("/businesses")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}


@router.delete("/businesses/{uuid}/delete")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}


@router.put("/businesses/{uuid}/details")
def update_business_details(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}


@router.get("/businesses/{uuid}/products")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}


@router.post("/businesses/{uuid}/products/add")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}


@router.post("/businesses/{uuid}/products/upload")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}


@router.patch("/businesses/{uuid}/toggle_favorite")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}
