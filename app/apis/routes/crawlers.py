from logging import Logger
from logging import getLogger
from typing import TYPE_CHECKING

from fastapi import APIRouter
from sqlmodel import select

from app.apis.deps.news import GetNewsDep
from app.apis.deps.session import SessionDep
from app.models.crawler import Crawler
from app.models.crawler import NewsPublic
from app.models.generic import SuccessMessage
from app.resources.crawler import fetch_news

if TYPE_CHECKING:
    from app.models.crawler import NewsItem

router = APIRouter(prefix="", tags=["crawlers"])


logger: Logger = getLogger(__name__)


@router.post("", response_model=SuccessMessage)
async def crawl_news(session: SessionDep) -> None:
    """'
    Fetch target news websites and fetch news items.
    """

    news_items: list[NewsItem] = fetch_news()

    for n in news_items:
        # TODO  Need to check if the news item already exists in the database
        news_item: Crawler = Crawler.model_validate(n, update={"creator_id": 1})  # I'm lazy.

        session.add(news_item)
        session.flush()

    session.commit()


@router.get("/{news_id}")
async def get_single_new(news: GetNewsDep) -> SuccessMessage[NewsPublic]:
    """
    Get a single news item.
    """
    return SuccessMessage(data=news)


@router.get("/")
async def get_news(session: SessionDep) -> SuccessMessage[list[NewsPublic]]:
    """
    Get all news items.
    """
    news: list[Crawler] = session.exec(select(Crawler)).all()

    return SuccessMessage(data=news)
