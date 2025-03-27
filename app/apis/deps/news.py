from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from sqlmodel import select

from app.models.crawler import Crawler

from .session import SessionDep


def get_news(session: SessionDep, news_id: int) -> Crawler:
    new: Crawler = session.exec(select(Crawler).where(Crawler.id == news_id)).first()

    if not new:
        raise HTTPException(status_code=404, detail="News not found")

    return new


GetNewsDep = Annotated[None, Depends(get_news)]
