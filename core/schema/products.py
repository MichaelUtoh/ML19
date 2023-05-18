from datetime import datetime

from pydantic import BaseModel


class ProductListSchema(BaseModel):
    id: int
    name: str
    product_no: str
    description: str
    created_timestamp: datetime


class ProductCreateUpdateSchema(BaseModel):
    name: str
    product_no: str
    description: str
