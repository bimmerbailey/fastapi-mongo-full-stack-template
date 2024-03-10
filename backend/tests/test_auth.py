import pytest
from httpx import AsyncClient
from jose import jwt

from app import schemas

users_url = "/api/v1/users"
auth_url = "/api/v1/login"


@pytest.mark.anyio
async def test_create_user(authorized_admin_client: AsyncClient, db):
    res = await authorized_admin_client.post(
        users_url, json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.users.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


@pytest.mark.anyio
async def test_login_user(db, client: AsyncClient, create_user, jwt_settings):
    user = await create_user()
    res = await client.post(
        auth_url,
        data={"username": user.email, "password": "password"},
    )
    login_res = schemas.users.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        jwt_settings.secret_key.get_secret_value(),
        algorithms=[jwt_settings.algorithm],
    )

    user_id = payload.get("user_id")
    token_data = schemas.users.TokenData(id=user_id)
    assert token_data
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.anyio
@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 401),
        ("michael@gmail.com", "wrongpassword", 401),
        ("wrongemail@gmail.com", "wrongpassword", 401),
        (None, "password123", 422),
        ("michael@gmail.com", None, 422),
    ],
)
async def test_incorrect_login(
    db, client: AsyncClient, email: str, password: str, status_code: int
):
    res = await client.post(auth_url, data={"username": email, "password": password})

    assert res.status_code == status_code
