from collections.abc import AsyncGenerator
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings


def get_db() -> Generator[Session, None, None]:
    from app.core.database import engine

    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


# 創建非同步資料庫引擎
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    # from app.core.database import engine
    engine = create_async_engine(str(settings.database.uri), echo=True)

    async with AsyncSession(engine) as session:
        yield session  # ⚠ 這裡要用 async with 確保正確關閉


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_db)]
