from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, status, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from app import schemas, models, crud
from app.config.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.users.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(
    header_token: Optional[str] = Depends(oauth2_scheme),
    token: Optional[str] = Cookie(default=None),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(header_token, credentials_exception)
    auth_user = await crud.users.user.get_one(token.id)

    return auth_user


def get_current_active_user(
    current_user: models.users.Users = Depends(get_current_user),
) -> models.users.Users:
    if not crud.users.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.users.Users = Depends(get_current_user),
) -> models.users.Users:
    if not crud.users.user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
