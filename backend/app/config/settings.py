import os

from pydantic import MongoDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True)
    debug: bool = False


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True, env_prefix="DATABASE_")

    hostname: str = "mongo"
    port: int = 27017
    password: SecretStr = "password"
    name: str = "your_app"
    username: str = "app_user"

    @property
    def database_url(self) -> MongoDsn:
        if not os.environ.get("DATABASE_URL", None):
            return MongoDsn(
                f"mongodb://{self.username}:{self.password.get_secret_value()}@"
                f"{self.hostname}:{self.port}/{self.name}"
            )
        return MongoDsn(os.environ.get("DATABASE_URL"))


class JwtSettings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True, env_prefix="JWT_")

    secret_key: SecretStr = "secret"
    algorithm: str = "HS256"
    token_expires: int = 60
    url_base: str = "localhost"


def get_app_settings() -> AppSettings:
    return AppSettings()


def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()


def get_jwt_settings() -> JwtSettings:
    return JwtSettings()
