import os
from collections.abc import Generator
from contextlib import contextmanager
from io import StringIO
from logging import Logger
from logging import getLogger

from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.runtime.environment import MigrationContext
from alembic.runtime.migration import MigrationStep
from alembic.script import ScriptDirectory
from sqlmodel import Field
from sqlmodel import SQLModel

from app.core.config import settings

logger: Logger = getLogger(__name__)


class AlembicVersion(SQLModel, table=True):
    __tablename__ = "alembic_version"
    version_num: str = Field(primary_key=True, max_length=32)


@contextmanager
def _buffer_redirect(config: Config) -> Generator[StringIO, None, None]:
    with StringIO() as buffer:
        _original_stdout = config.stdout
        config.stdout = buffer
        yield buffer
        config.stdout = _original_stdout


def get_alembic_config() -> Config:
    config: Config = Config(settings.PROJECT_DIR / "alembic.ini")
    config.set_main_option("sqlalchemy.url", str(settings.database.uri))

    if not os.access((script_location := config.get_main_option("script_location")), os.F_OK):
        config.set_main_option("script_location", str(settings.PROJECT_DIR / script_location))

    return config


def get_alembic_script(config: Config = None) -> ScriptDirectory:
    if not config:
        config = get_alembic_config()

    return ScriptDirectory.from_config(config)


def heads(script: ScriptDirectory = None) -> str:
    if not script:
        script = get_alembic_script()

    return script.get_current_head()


def current(config: Config = None) -> str:
    if not config:
        config = get_alembic_config()

    with _buffer_redirect(config) as buffer:
        script = ScriptDirectory.from_config(config)

        def get_current(rev: tuple[str, ...], _: MigrationContext) -> list[MigrationStep]:
            config.print_stdout(rev[0] if rev != () else "")
            return []

        with EnvironmentContext(config, script, fn=get_current, dont_mutate=True):
            script.run_env()

        buffer.seek(0)
        return buffer.read().strip()
