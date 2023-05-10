from pydantic import BaseModel

class ProductListSchema(BaseModel):
    id: int
    name: str
    product_no: str
    description: str
    business_id: int


class ProductCreateUpdateSchema(BaseModel):
    name: str
    product_no: str
    description: str
    business_id: int
