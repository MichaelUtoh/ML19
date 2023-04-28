from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class AuthFindSchema(BaseModel):
    email: Optional[EmailStr] = "a@a.com"


class AuthPassSchema(AuthFindSchema):
    first_name: Optional[str]
    middle_name: Optional[str]
    token: Optional[str] = None


class UserCreateBasicSchema(BaseModel):
    email: EmailStr
    password: str  # Hash


class UserUpdateSchema(BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    status: Optional[str]
    phone: Optional[str]
    address1: Optional[str]
    address2: Optional[str]
    next_of_kin_first_name: Optional[str]
    next_of_kin_last_name: Optional[str]
    next_of_kin_phone: Optional[str]
    next_of_kin_address: Optional[str]


class UserDetailSchema(AuthFindSchema):
    id: int
    uuid: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    status: Optional[str]
    phone: Optional[str]
    address1: Optional[str]
    address2: Optional[str]
    next_of_kin_first_name: Optional[str]
    next_of_kin_last_name: Optional[str]
    next_of_kin_phone: Optional[str]
    next_of_kin_address: Optional[str]
    timestamp: Optional[datetime] = None
