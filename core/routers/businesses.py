import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.schema.businesses import (
    BusinessCreateSchema,
    BusinessDetailListSchema,
    IdListSchema,
    LocationDetailSchema,
    LocationSchema,
)
from core.schema.products import ProductCreateUpdateSchema
from core.services.businesses import (
    add_business_products,
    business_create_func,
    business_delete_func,
    business_list_func,
    business_logo_func,
    business_obj_func,
    business_update_func,
    get_business_products_func,
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


@router.get("/locations", response_model=List[LocationDetailSchema])
def get_location(
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = locations_list_func(user, session)
    return data


@router.get("/businesses", response_model=List[BusinessDetailListSchema])
def businesses(
    # uuid: Optional[str] = None,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = business_list_func(uuid, user, session)
    return data


@router.post("/businesses/create")
def businesses(
    data: BusinessCreateSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = business_create_func(data, user, session)
    return data


@router.patch("/businesses/delete", status_code=204)
def delete_business(
    ids: IdListSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    business_delete_func(ids, user, session)
    return


@router.get("/businesses/{uuid}/details", response_model=BusinessDetailListSchema)
def businesses(
    uuid: Optional[str] = None,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = business_obj_func(uuid, user, session)
    return data


@router.put("/businesses/{uuid}/update", response_model=BusinessDetailListSchema)
def update_business_details(
    uuid: str,
    data: BusinessCreateSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = business_update_func(uuid, data, user, session)
    return data


@router.post(
    "/businesses/{uuid}/add_logo",
    response_model=BusinessDetailListSchema,
    status_code=200,
)
def update_business_details(
    uuid: str,
    file: UploadFile = File(),
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = business_logo_func(uuid, file, user, session)
    return data


@router.get("/businesses/{uuid}/products")
def get_products(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    get_business_products_func(uuid, user, session)
    return {}


@router.post("/businesses/{uuid}/products/add")
def add_products(
    uuid: str,
    data: ProductCreateUpdateSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    add_business_products(uuid, data, user, session)
    return {}


@router.post("/businesses/{uuid}/products/upload")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}


@router.get("/businesses/{uuid}/reviews")
def business_reviews(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
):
    return {}


@router.post("/businesses/{uuid}/reviews/add")
def business_reviews(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
):
    return {}


@router.patch("/businesses/{uuid}/toggle_favorite")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}
