import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LocationDetailSchema(BaseModel):
    id: int
    state: str
    capital: str
    created_timestamp: Optional[datetime] = None


class LocationSchema(BaseModel):
    state: str
    capital: str


class BusinessCreateSchema(BaseModel):
    name: str
    logo: Optional[str]
    description: Optional[str]
    open_days: Optional[list[str]] = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
    ]
    address: str
    location: int
