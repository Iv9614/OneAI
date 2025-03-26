import os
from logging import Logger
from logging import getLogger
from typing import TYPE_CHECKING

from alembic.command import upgrade
from sqlalchemy import Engine
from sqlalchemy import MetaData
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import drop_database
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel import create_engine
from sqlmodel import select

from app.core.config import settings

# metadata 是一個 資料表的結構總表, 裡面紀錄了所有的 Table、Column、Constraint 等等資料。
# 只有 已經載入到 Python 記憶體中的 model classes, 才會註冊到 metadata。
# 如果你沒 import 某個 model, 它不會被載入 → SQLModel 不知道它存在 → 它不會出現在 metadata → create_all() 不會幫你建立這張表。
from app.models.databases import *

from .helpers import current
from .helpers import get_alembic_config
from .helpers import get_alembic_script
from .helpers import heads
from .initial import inject_initial_data

if TYPE_CHECKING:
    from alembic.config import Config
    from alembic.script import ScriptDirectory


logger: Logger = getLogger(__name__)


engine: Engine = create_engine(str(settings.database.uri))
metadata: MetaData = SQLModel.metadata


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28
async def init_database() -> None:
    config: Config = get_alembic_config()
    script: ScriptDirectory = get_alembic_script(config)

    head: str = heads(script)
    if not database_exists(engine.url):
        try:
            logger.info("Database not exist, creating database...")
            create_database(engine.url)
            logger.info("Database created successfully.")

        except OperationalError as e:
            logger.error("Database creation failed. Force exit...")
            logger.error("Error: %s", e)

            exit(1)

        try:
            logger.info("Running migrates...")
            upgrade(config, "head")

            with Session(engine) as session:
                await inject_initial_data(session=session)

        except Exception as e:  # noqa: BLE001
            logger.error("Database creation failed.")
            logger.error("Error: %s", e)
            logger.error("Dropping database...")

            if not isinstance(e, OperationalError):
                drop_database(engine.url)

            exit(1)

    _current = current(config)
    logger.info("Current database revision: %s", _current)

    if _current != head:
        logger.info("Upgrading database to latest version...")
        upgrade(config, "head")

    logger.info("Database migration complete.")
