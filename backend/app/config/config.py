import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname = os.environ.get("DATABASE_HOST", "mongo")
    database_port = os.environ.get("DATABASE_PORT", "27017")
    database_password = os.environ.get("DATABASE_PASSWORD", "password")
    database_name = os.environ.get("DATABASE_NAME", "test_your_app")
    database_username = os.environ.get("DATABASE_USERNAME", "app_user")
    secret_key = os.environ.get("JWT_SECRET_KEY", "secret")
    algorithm = os.environ.get("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes = os.environ.get("JWT_TOKEN_EXPIRES", 60)
    url_base = os.environ.get("URL_BASE", "localhost")

    database_url = os.environ.get("DATABASE_URL",
                                  f"mongodb://{database_username}:{database_password}@{database_hostname}/"
                                  f"{database_name}?retryWrites=true&w=majority")


settings = Settings()
