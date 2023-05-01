from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class UserStatus(str, Enum):
    ADMIN = "admin"
    BUSINESS_OWNER = "business owner"
    CUSTOMER = "customer"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(default=None, unique=True)
    password: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[UserStatus] = UserStatus.CUSTOMER
    phone: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    next_of_kin_first_name: Optional[str] = None
    next_of_kin_last_name: Optional[str] = None
    next_of_kin_phone: Optional[str] = None
    next_of_kin_address: Optional[str] = None
    businesses: List["Business"] = Relationship(back_populates="user")
    created_timestamp: Optional[datetime] = Field(default=datetime.utcnow())
    updated_timestamp: Optional[datetime] = Field(default=datetime.utcnow())

    class Config:
        orm_mode = True
