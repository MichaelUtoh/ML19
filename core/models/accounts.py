import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr

from sqlmodel import Field, SQLModel, create_engine


class UserStatus(str, Enum):
    LEVEL_1 = "Level 1"
    LEVEL_2 = "Level 2"
    LEVEL_3 = "Level 3"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(default=None, unique=True)
    password: str
    uuid: Optional[str] = uuid.uuid4()
    username: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    next_of_kin_first_name: Optional[str] = None
    next_of_kin_last_name: Optional[str] = None
    next_of_kin_phone: Optional[str] = None
    next_of_kin_address: Optional[str] = None
    timestamp: Optional[datetime] = datetime.now()
