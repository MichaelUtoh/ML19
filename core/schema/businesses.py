import uuid
from typing import Optional

from pydantic import BaseModel


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
