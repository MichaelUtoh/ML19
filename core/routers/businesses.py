import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.schema.businesses import (
    BusinessCreateSchema,
    LocationDetailSchema,
    LocationSchema,
)
from core.services.businesses import (
    business_create_func,
    business_list_func,
    locations_create_func,
    locations_list_func,
)


auth_handler = AuthHandler()
router = APIRouter(tags=["Business"])


@router.post("/locations/add", response_model=LocationDetailSchema)
def add_location(
    data: LocationSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = locations_create_func(data, user, session)
    return data


@router.get("/locations")
def get_location(
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = locations_list_func(user, session)
    return data


@router.get("/businesses")
def businesses(
    uuid: Optional[str] = None,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = business_list_func(uuid, user, session)
    return data


@router.post("/businesses/add")
def businesses(
    data: BusinessCreateSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = business_create_func(data, user, session)
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
