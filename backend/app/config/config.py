from pydantic import ConfigDict, MongoDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(frozen=True)

    database_hostname: str = "mongo"
    database_port: int = 27017
    database_password: str = "password"
    database_name: str = "your_app"
    database_username: str = "app_user"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    jwt_token_expires: int = 60
    url_base: str = "localhost"
    log_level: str = "DEBUG"
    json_logs: bool = False

    database_url: MongoDsn = (
        f"mongodb://{database_hostname}:{database_port}/{database_name}"
    )


settings = Settings()
