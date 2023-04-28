import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Location(SQLModel, table=True):
    id: int = Field(primary_key=True)
    state: str
    capital: str


class Business(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: Optional[str] = uuid.uuid4()
    name: str
    description: Optional[str] = None
    owner: int
    address: str
    location_id: int = Field(foreign_key="location.id")
    location: Location = Relationship(back_populates="businesses")
