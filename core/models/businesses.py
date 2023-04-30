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
    logo: Optional[str] = None
    description: Optional[str] = None
    open_days: list[str]
    address: str
    location_id: int = Field(foreign_key="location.id")
    location: Location = Relationship(back_populates="businesses")
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # class Config:
    #     arbitrary_types_allowed = True