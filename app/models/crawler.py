from typing import TYPE_CHECKING

from sqlalchemy_utils.types.arrow import ArrowType
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

from .common import ArrowPydanticV2
from .common import DatetimeMixin

if TYPE_CHECKING:
    from .user import User


class CrawlerBase(SQLModel):
    title: str
    link: str

    news_time: ArrowPydanticV2 = Field(nullable=True, sa_type=ArrowType, default=None)


class NewsItem(CrawlerBase):
    pass


class NewsPublic(CrawlerBase, DatetimeMixin):
    creator_id: int | None = Field(nullable=True)


class Crawler(CrawlerBase, DatetimeMixin, table=True):
    __tablename__ = "crawler"

    id: int = Field(default=None, primary_key=True)

    creator_id: int = Field(nullable=True, foreign_key="users.id", ondelete="SET NULL")
    creator: "User" = Relationship(back_populates="crawler")
