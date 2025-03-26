from datetime import datetime

from pydantic import BaseModel
from pydantic import HttpUrl
from pydantic import field_validator
from sqlalchemy_utils.types.arrow import ArrowType
from sqlmodel import Field
from sqlmodel import SQLModel

from .common import ArrowPydanticV2


# Input Schema
class URLRequest(BaseModel):
    original_url: HttpUrl

    @field_validator("original_url", mode="before")
    @classmethod
    def check_length(cls, v: str) -> str:
        if len(v) > 2048:
            raise ValueError("URL is invalid, due to length is too long.")

        return v


# Output Schema
class URLResponse(BaseModel):
    short_url: str = ""
    expiration_date: datetime = None
    success: bool
    reason: str = None


class UrlsBase(SQLModel, table=True):
    __tablename__ = "urls"

    id: int = Field(default=None, primary_key=True)

    original_url: str | None = Field(nullable=False, index=True, max_length=2048)
    short_url: str | None = Field(nullable=False, index=True, max_length=2048)

    expiration_date: ArrowPydanticV2 | None = Field(nullable=True, sa_type=ArrowType, default=None)
    created_at: ArrowPydanticV2 | None = Field(nullable=True, sa_type=ArrowType, default=None)
    updated_at: ArrowPydanticV2 | None = Field(nullable=True, sa_type=ArrowType, default=None)
