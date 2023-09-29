import pytest
from jose import jwt
from httpx import AsyncClient

from app import schemas
from app.config.config import settings
from app.models.users import Users

users_url = "/api/v1/users"
auth_url = "/api/v1/login"


@pytest.mark.anyio
async def test_create_user(client: AsyncClient, db):
    res = await client.post(
        users_url, json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.users.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


@pytest.mark.anyio
async def test_login_user(db, client: AsyncClient, regular_user: Users):
    res = await client.post(
        auth_url, data={"username": regular_user.email, "password": regular_user.password})
    login_res = schemas.users.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])

    user_id = payload.get("user_id")
    token_data = schemas.users.TokenData(id=user_id)

    # assert regular_user.id == token_data.id
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.anyio
async def test_admin(db, client: AsyncClient, admin_user: Users):
    res = await client.post(
        auth_url, data={"username": admin_user.email, "password": admin_user.password})
    login_res = schemas.users.Token(**res.json())
    assert res.status_code == 200
    assert login_res.is_admin


@pytest.mark.anyio
async def test_regular_user(db, client: AsyncClient, regular_user: Users):
    res = await client.post(
        auth_url, data={"username": regular_user.email, "password": regular_user.password})
    login_res = schemas.users.Token(**res.json())
    assert res.status_code == 200
    assert not login_res.is_admin


@pytest.mark.anyio
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 401),
    ('michael@gmail.com', 'wrongpassword', 401),
    ('wrongemail@gmail.com', 'wrongpassword', 401),
    (None, 'password123', 422),
    ('michael@gmail.com', None, 422)
])
async def test_incorrect_login(db, client: AsyncClient, email: str, password: str, status_code: int):
    res = await client.post(
        auth_url, data={"username": email, "password": password})

    assert res.status_code == status_code
