from logging import Logger
from logging import getLogger
from pathlib import Path

from pydantic import PostgresDsn
from pydantic import SecretStr
from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict
from pydantic_settings import YamlConfigSettingsSource

logger: Logger = getLogger(__name__)

_PROJECT_DIR: Path = Path(__file__).parent.parent.parent


class SenaoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
    )

    def reload(self) -> None:
        """Helper function to reload the settings."""
        # See: https://docs.pydantic.dev/latest/concepts/pydantic_settings/#in-place-reloading
        self.__init__()


class ProjectSetting(SenaoSettings):
    name: str = "Senao"


class DatabaseSettings(SenaoSettings):
    server: str
    port: int = 5432
    user: str = "postgres"
    password: SecretStr
    database: str = "postgres"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.server,
            port=self.port,
            path=self.database,
        )


class Settings(SenaoSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_ignore_empty=True,
        env_nested_delimiter="__",
        yaml_file="env.yaml",
        extra="ignore",
    )

    PROJECT_DIR: Path = _PROJECT_DIR

    project: ProjectSetting
    database: DatabaseSettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            YamlConfigSettingsSource(settings_cls),
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


settings: Settings = Settings()
# logger.info("Database URI: %s", util.obfuscate_url_pw(str(settings.database.uri)))
