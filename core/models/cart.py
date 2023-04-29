from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: Optional[str]
    price: float
    available_quantity: int


class Cart(SQLModel, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    user_id: int
    items: List["CartItem"] = Field(default_factory=list)


class CartItem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    cart_id: int
    product_id: int
    quantity: int
