from typing import AsyncIterable

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from jose import jwt

from app.config.settings import (
    DatabaseSettings,
    JwtSettings,
    get_jwt_settings,
)
from app.dependencies.auth import CryptContext, get_crypt_context
from app.dependencies.database import close_mongo_connection, connect_to_mongo
from app.main import init_app
from app.models.users import User
from app.schemas.users import Token, TokenData


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def db_settings() -> DatabaseSettings:
    return DatabaseSettings()


@pytest.fixture
async def db(anyio_backend: str):
    motor_client = await connect_to_mongo()
    database = motor_client.get_default_database()
    try:
        yield database
    finally:
        for collection in await database.list_collection_names():
            await database.drop_collection(collection)
        await close_mongo_connection(motor_client)


@pytest.fixture
async def app() -> FastAPI:
    return init_app()


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test-client:8000"
    ) as client:
        yield client


@pytest.fixture
def crpyt() -> CryptContext:
    return get_crypt_context()


@pytest.fixture
def jwt_settings() -> JwtSettings:
    return get_jwt_settings()


@pytest.fixture
def create_user(db, crpyt):
    async def _create_user(
        password="password", email="user@example.com", is_admin=False
    ) -> User:
        user = User(
            email=email,
            password=crpyt.hash(password),
            first_name="test",
            last_name="user",
            is_admin=is_admin,
        )
        await user.save()
        return user

    return _create_user


@pytest.fixture
def authorize_client(client: AsyncClient):
    async def _authorize_client(user: User, password: str):
        return await client.post(
            "api/v1/login", data={"username": user.email, "password": password}
        )

    return _authorize_client


@pytest.fixture
async def authorized_admin_client(
    client, create_user, jwt_settings, authorize_client
) -> AsyncIterable[AsyncClient]:
    user = await create_user(is_admin=True)
    res = await authorize_client(user, "password")

    login_res = Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        jwt_settings.secret_key.get_secret_value(),
        algorithms=[jwt_settings.algorithm],
    )

    user_id = payload.get("user_id")
    token_data = TokenData(id=user_id)
    assert token_data

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {login_res.access_token}",
    }
    yield client


@pytest.fixture
async def authorized_regular_client(
    client: AsyncClient, create_user, jwt_settings, authorize_client
) -> AsyncIterable[AsyncClient]:
    user = await create_user(is_admin=False)
    res = await authorize_client(user, "password")

    login_res = Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        jwt_settings.secret_key.get_secret_value(),
        algorithms=[jwt_settings.algorithm],
    )

    user_id = payload.get("user_id")
    token_data = TokenData(id=user_id)
    assert token_data

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {login_res.access_token}",
    }
    yield client
