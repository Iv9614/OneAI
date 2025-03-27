from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from .crawler import Crawler


class UserBase(SQLModel):
    email: str | None = Field(nullable=False, index=True)

    username: str | None = Field(nullable=False, max_length=50)

    is_active: bool = Field(default=True)

    full_name: str | None = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str | None = Field(nullable=False, max_length=50)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    # password: str|None = Field(nullable=False, max_length=50)
    hashed_password: str

    crawler: list["Crawler"] = Relationship(back_populates="creator")
