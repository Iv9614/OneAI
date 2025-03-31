from logging import Logger
from logging import getLogger
from typing import TYPE_CHECKING

from pydantic import HttpUrl
from sqlalchemy.exc import OperationalError
from sqlmodel import Session
from sqlmodel import delete

from app.models.crawler import Crawler

if TYPE_CHECKING:
    from app.models.crawler import NewsItem


logger: Logger = getLogger(__name__)


async def create_feature_news(*, session: Session, target_url: HttpUrl) -> None:
    from app.resources.crawler import fetch_news

    news_items: list[NewsItem] = await fetch_news(session=session, url=target_url)

    try:
        for n in news_items:
            # TODO  Need to check if the news item already exists in the database
            news_item: Crawler = Crawler.model_validate(n, update={"creator_id": 1})  # I'm lazy so just use admin user.

            session.add(news_item)
            session.flush()

        logger.info("Crawler %s created successfully.", target_url)

        session.commit()

    except OperationalError as e:
        logger.error(e)
        session.rollback()

        exit(1)


def delete_all_news(session: Session) -> None:
    """
    Delete all news items from the database.

    :param session: The database session.

    """
    try:
        session.exec(delete(Crawler))
        session.commit()

    except OperationalError as e:
        logger.error("Delete news failed: %s", e)
        session.rollback()

    logger.info("Successfully deleted all news items.")
