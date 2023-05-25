import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_pagination import Page
from sqlalchemy.orm import Session as SQA_Session

from core.config.auth import AuthHandler
from core.config.database import get_session
from core.schema.businesses import (
    BusinessCreateSchema,
    BusinessDetailListSchema,
    BusinessProductsSchema,
    BusinessReviewCreateSchema,
    IdListSchema,
    LocationDetailSchema,
    LocationSchema,
)
from core.schema.products import ProductCreateUpdateSchema, ProductListSchema
from core.services.businesses import (
    add_business_products_func,
    add_business_review_func,
    batch_upload_func,
    business_create_func,
    business_delete_func,
    business_list_func,
    business_logo_func,
    business_obj_func,
    business_update_func,
    get_business_products_func,
    get_business_review_func,
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


@router.get("/businesses", response_model=Page[BusinessDetailListSchema])
def businesses(
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = business_list_func(user, session)
    return data


@router.post("/businesses/create", response_model=BusinessDetailListSchema)
def businesses(
    data: BusinessCreateSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    data = business_create_func(data, user, session)
    return data


@router.delete("/businesses/delete", status_code=204)
def delete_business(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return business_delete_func(uuid, user, session)


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


@router.get("/businesses/{uuid}/products", response_model=Page[ProductListSchema])
def get_products(
    uuid: str,
    email=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return get_business_products_func(uuid, email, session)


@router.post("/businesses/{uuid}/products/add", response_model=ProductListSchema)
def add_products(
    uuid: str,
    data: ProductCreateUpdateSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return add_business_products_func(uuid, data, user, session)


@router.post(
    "/businesses/{uuid}/products/upload",
)  # response_model=ProductListSchema)
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    file: UploadFile = File(),
    session: SQA_Session = Depends(get_session),
):
    return batch_upload_func(uuid, user, file, session)


@router.get("/businesses/{uuid}/reviews")
def business_reviews(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return get_business_review_func(uuid, user, session)


@router.post("/businesses/{uuid}/reviews/add")
def business_reviews(
    uuid: str,
    data: BusinessReviewCreateSchema,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return add_business_review_func(uuid, data, user, session)


@router.patch("/businesses/{uuid}/toggle_favorite")
def businesses(
    uuid: str,
    user=Depends(auth_handler.auth_wrapper),
    session: SQA_Session = Depends(get_session),
):
    return {}
