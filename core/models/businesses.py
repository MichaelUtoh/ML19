import uuid
from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from core.models.accounts import User


class Location(SQLModel, table=True):
    id: int = Field(primary_key=True)
    state: str
    capital: str
    businesses: List["Business"] = Relationship(back_populates="location")
    created_timestamp: Optional[datetime] = Field(default=datetime.utcnow())
    updated_timestamp: Optional[datetime] = Field(default=datetime.utcnow())


class Business(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: Optional[str] = uuid.uuid4()
    name: str
    logo: Optional[str] = None
    description: Optional[str] = None
    open_days: list[str]
    address: str
    location_id: int = Field(default=None, foreign_key="location.id")
    location: Optional[Location] = Relationship(back_populates="businesses")
    profile_id: Optional[int] = Field(default=None, foreign_key="profile.id")
    # profile: Optional[User] = Relationship(back_populates="businesses")
    products: List["Product"] = Relationship(back_populates="business")
    reviews: List["Review"] = Relationship(back_populates="business")
    created_timestamp: Optional[datetime] = Field(default=datetime.utcnow())
    updated_timestamp: Optional[datetime] = Field(default=datetime.utcnow())

    class Config:
        orm_mode = True


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    profile_id: Optional[int] = Field(default=None, foreign_key="profile.id")
    # profile: Optional[User] = Relationship(back_populates="reviews")
    business_id: Optional[int] = Field(default=None, foreign_key="business.id")
    business: Optional[Business] = Relationship(back_populates="reviews")
    created_timestamp: Optional[datetime] = Field(default=datetime.utcnow())
    updated_timestamp: Optional[datetime] = Field(default=datetime.utcnow())

