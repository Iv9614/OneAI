import logging

from sqlmodel import Session

from app.crud.crawler import create_feature_news
from app.crud.user import create_user

logger = logging.getLogger(__name__)


async def inject_initial_data(*, session: Session) -> None:
    # Inject init user
    logger.info("Injecting initial user...")
    create_user(session=session)

    # Inject init feature news
    logger.info("Injecting initial feature news...")
    await create_feature_news(session=session, target_url="https://tw-nba.udn.com/nba/index")
