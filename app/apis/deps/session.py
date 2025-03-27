from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session


def get_db() -> Generator[Session, None, None]:
    from app.core.database import engine

    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
