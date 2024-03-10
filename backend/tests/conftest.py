import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.database.init_db import close_mongo_connection, connect_to_mongo
from app.main import init_app
from app.models.users import Users


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def motor_client(anyio_backend) -> AsyncIOMotorClient:
    return await connect_to_mongo()


@pytest.fixture
async def db(anyio_backend: str, motor_client: AsyncIOMotorClient):
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
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test-client:8000") as client:
        yield client


@pytest.fixture
async def regular_user(client: AsyncClient):
    user_data = {"email": "user@gmail.com", "password": "password123"}
    res = await client.post("api/v1/users", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return Users(**new_user)


@pytest.fixture
async def admin_user(client: AsyncClient):
    user_data = {
        "email": "admin@gmail.com",
        "password": "password123",
        "is_admin": "true",
    }
    res = await client.post("api/v1/users", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return Users(**new_user)


@pytest.fixture
def token(test_user):
    return oauth.create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client: AsyncClient, token: str):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client
