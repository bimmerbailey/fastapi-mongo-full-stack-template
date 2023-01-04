import asyncio
from httpx import AsyncClient
import pytest

from app.main import app
from app.database.init_db import db_client, connect_to_mongo
from app import oauth
from app.models.users import User


@pytest.fixture(scope="class")
def event_loop_instance(request):
    """ Add the event_loop as an attribute to the unittest style test class. """
    request.cls.event_loop = asyncio.get_event_loop_policy().new_event_loop()
    yield
    request.cls.event_loop.close()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    await connect_to_mongo()
    db = db_client.get_db()
    await db.drop_collection("users")

    async with AsyncClient(app=app, base_url="http://localhost:3000") as client:
        yield client


@pytest.fixture
@pytest.mark.anyio
async def regular_user(client: AsyncClient):
    db = db_client.get_db()
    await db.drop_collection("users")

    user_data = {"email": "user@gmail.com",
                 "password": "password123"}
    res = await client.post("api/v1/users", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return User(**new_user)


@pytest.fixture
@pytest.mark.anyio
async def admin_user(client: AsyncClient):
    db = db_client.get_db()
    await db.drop_collection("users")

    user_data = {"email": "admin@gmail.com",
                 "password": "password123",
                 "is_admin": "true"}
    res = await client.post("api/v1/users", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return User(**new_user)


@pytest.fixture
def token(test_user):
    return oauth.create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client: AsyncClient, token: str):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client
