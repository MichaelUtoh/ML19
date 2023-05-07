from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    product_no: str
    description: str
    created_timestamp: Optional[datetime] = Field(default=datetime.utcnow())
    updated_timestamp: Optional[datetime] = Field(default=datetime.utcnow())
