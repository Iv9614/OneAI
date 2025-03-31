import re
from logging import Logger
from logging import getLogger
from typing import TYPE_CHECKING

import arrow
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from pydantic import HttpUrl
from sqlmodel import Session

from app.crud.crawler import delete_all_news
from app.models.crawler import NewsItem

logger: Logger = getLogger(__name__)

if TYPE_CHECKING:
    from bs4.element import Tag

# URL of the NBA page
url = "https://tw-nba.udn.com/nba/index"

# Set headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

PARSE_HOUR_PATTERN = r"(\d+)小時"
PARSE_MIN_PATTERN = r"(\d+)分鐘"


def parse_news_time(news_time: str) -> arrow.Arrow:
    """
    Use regex to parse the news time string and return an Arrow object.

    :param news_time: The time string to parse.
    :return: An Arrow object representing the parsed time.
    """

    parse_time: arrow.Arrow = arrow.utcnow()

    if re.findall("[\u4e00-\u9fa5]+", news_time):  # Check if the string contains Chinese characters
        if match := re.search(PARSE_MIN_PATTERN, news_time):
            logger.info("found minute pattern: %s", match.group(0))

            shift_time: int = int(match.group(1))

            parse_time = arrow.utcnow().shift(minutes=-shift_time)

        elif match := re.search(PARSE_HOUR_PATTERN, news_time):
            logger.info("found hour pattern: %s", match.group(0))
            shift_time: int = int(match.group(1))

            parse_time = arrow.utcnow().shift(hours=-shift_time)

    else:
        try:
            logger.info("found date pattern: %s", news_time)
            parse_time = arrow.get(news_time)

        except arrow.parser.ParserError:
            logger.error("解析時間失敗: %s", news_time)

            raise HTTPException(status_code=400, detail="解析時間失敗")

    return parse_time


async def fetch_news(*, session: Session, url: HttpUrl) -> list[NewsItem]:
    """
    Fetch news from the given URL and return a list of NewsItem objects.

    :param session: The database session to use.
    :param url: The URL to fetch news from.

    :return: A list of NewsItem objects.

    """

    news_list: list = []

    response = requests.get(url, headers=headers, timeout=5)
    response.encoding = "utf-8"

    if response.status_code // 100 != 2:
        logger.error("請求失敗, 狀態碼: %s", response.status_code)

        raise HTTPException(status_code=response.status_code, detail="請求失敗")

    delete_all_news(session=session)

    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

    featured_section: Tag = soup.find("div", class_="box_body")

    if featured_section:
        logger.info("Finding featured section.")

        news_items: Tag = featured_section.find_all("a")

        for item in news_items:
            time_tag: Tag = item.find("b", class_="h24")
            news_create_time: str = time_tag.get_text(strip=True) if time_tag else "None"

            news_list.append(
                NewsItem(
                    title=item.get_text(strip=True), link=item["href"], news_time=parse_news_time(news_create_time)
                )
            )

    else:
        logger.error("Not found featured section.")

    return news_list
