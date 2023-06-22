from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from core.models.businesses import Business


class Cart(SQLModel, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    user_id: int
    items: List["CartItem"] = Field(default_factory=list)


class CartItem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    cart_id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    quantity: int


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    product_no: str
    description: str
    business_id: Optional[int] = Field(default=None, foreign_key="business.id")
    business: Optional[Business] = Relationship(back_populates="products")
    created_timestamp: Optional[datetime] = Field(default=datetime.utcnow())
    updated_timestamp: Optional[datetime] = Field(default=datetime.utcnow())
