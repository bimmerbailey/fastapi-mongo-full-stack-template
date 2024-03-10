import logging
from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config.settings import JwtSettings, get_jwt_settings
from app.models.users import User
from app.schemas.users import TokenData

logging.getLogger("passlib").setLevel(logging.ERROR)


def get_crypt_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def create_access_token(
    data: dict, settings: Annotated[JwtSettings, Depends(get_jwt_settings)]
):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.token_expires)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm
    )

    return encoded_jwt


def verify_access_token(
    token: str, settings: Annotated[JwtSettings, Depends(get_jwt_settings)]
) -> Optional[TokenData]:
    try:
        payload = jwt.decode(
            token, settings.secret_key.get_secret_value(), algorithms=settings.algorithm
        )
        user_id: str = payload.get("user_id")
        if user_id is None:
            return None
        token_data = TokenData(id=user_id)
    except JWTError:
        return None
    return token_data


async def get_current_user(
    settings: Annotated[JwtSettings, Depends(get_jwt_settings)],
    header_token: Optional[str] = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(header_token, settings)
    if not token:
        raise credentials_exception
    user = await User.get(token.id)
    if not user:
        raise credentials_exception
    return user
