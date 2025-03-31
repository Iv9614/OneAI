from logging import Logger
from logging import getLogger

from fastapi import APIRouter

from app.apis.deps.news import GetNewsDep
from app.apis.deps.news import GetNewsListDep
from app.apis.deps.session import SessionDep
from app.crud.crawler import create_feature_news
from app.models.crawler import CrawlNewsSchema
from app.models.crawler import NewsPublic
from app.models.generic import SuccessMessage

router = APIRouter(prefix="", tags=["crawlers"])


logger: Logger = getLogger(__name__)


@router.post("", response_model=SuccessMessage[str])
async def crawl_news(session: SessionDep, crawl_in: CrawlNewsSchema) -> None:
    """
    Fetch target news websites and fetch news items.
    """
    await create_feature_news(session=session, target_url=crawl_in.url)

    return SuccessMessage(data="Crawling completed.")


@router.get("/list", response_model=SuccessMessage[list[NewsPublic]])
async def get_news(all_news: GetNewsListDep) -> SuccessMessage[list[NewsPublic]]:
    """
    Get all news items.
    """
    return SuccessMessage(data=all_news)


@router.get("/{news_id}", response_model=SuccessMessage[NewsPublic])
async def get_single_new(news: GetNewsDep) -> SuccessMessage[NewsPublic]:
    """
    Get a single news item.
    """
    return SuccessMessage(data=news)
