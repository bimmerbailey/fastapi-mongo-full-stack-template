import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = os.environ.get("DATABASE_HOST", "mongo")
    database_port: str = os.environ.get("DATABASE_PORT", "27017")
    database_password: str = os.environ.get("DATABASE_PASSWORD", "password")
    database_name: str = os.environ.get("DATABASE_NAME", "your_app")
    database_username: str = os.environ.get("DATABASE_USERNAME", "app_user")
    secret_key: str = os.environ.get("JWT_SECRET_KEY", "secret")
    algorithm: str = os.environ.get("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = os.environ.get("JWT_TOKEN_EXPIRES", 60)
    url_base: str = os.environ.get("URL_BASE", "localhost")
    log_level: str = os.environ.get("LOG_LEVEL", "DEBUG")
    json_logs: bool = os.environ.get("JSON_LOGS", False)

    database_url: str = os.environ.get(
        "DATABASE_URL",
        f"mongodb://{database_username}:{database_password}@{database_hostname}/"
        f"{database_name}?retryWrites=true&w=majority",
    )


settings = Settings()
