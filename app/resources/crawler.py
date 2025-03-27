import re
from logging import Logger
from logging import getLogger
from typing import TYPE_CHECKING

import arrow
import requests
from bs4 import BeautifulSoup

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

PARSE_TIME_PATTERN = r"(\d+)小時"


def parse_news_time(news_time: str) -> arrow.Arrow:
    try:
        parse_time = arrow.get(news_time, "YYYY-MM-DD")

    except arrow.parser.ParserError:
        match = re.search(PARSE_TIME_PATTERN, news_time)

        if match:
            hours = int(match.group(1))

            parse_time = arrow.utcnow().shift(hours=-hours)

    return parse_time


def fetch_news() -> list[NewsItem]:
    news_list: list = []

    url = "https://tw-nba.udn.com/nba/index"

    response = requests.get(url, timeout=5)
    response.encoding = "utf-8"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        featured_section = soup.find("div", class_="box_body")

        if featured_section:
            news_items = featured_section.find_all("a")

            for item in news_items:
                time_tag: Tag = item.find("b", class_="h24")
                news_create_time: str = time_tag.get_text(strip=True) if time_tag else "None"

                NewsItem(title=item.get_text(strip=True), link=item["href"])

                news_list.append(
                    NewsItem(
                        title=item.get_text(strip=True), link=item["href"], news_time=parse_news_time(news_create_time)
                    )
                )

        else:
            logger.info("未找到精選新聞區塊。")
    else:
        logger.error("請求失敗, 狀態碼: %s", response.status_code)

    return news_list
