from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from app.config.settings import JwtSettings, get_jwt_settings
from app.dependencies.auth import (
    CryptContext,
    create_access_token,
    get_crypt_context,
    get_current_user,
)
from app.models.users import User
from app.schemas.users import Token, UserBase

router = APIRouter(tags=["Authentication"], prefix="/api/v1")
logger = structlog.stdlib.get_logger(__name__)


@router.post("/login", response_model=Token)
async def login(
    crypt_context: Annotated[CryptContext, Depends(get_crypt_context)],
    jwt_settings: Annotated[JwtSettings, Depends(get_jwt_settings)],
    user_credentials: OAuth2PasswordRequestForm = Depends(),
):
    auth_user = await User.get_by_email(email=user_credentials.username)
    if not auth_user or not crypt_context.verify(
        user_credentials.password, auth_user.password
    ):
        crypt_context.dummy_verify()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Credentials",
        )

    access_token = create_access_token(
        data={"user_id": str(auth_user.id)}, settings=jwt_settings
    )

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "is_admin": auth_user.is_admin,
        }
    )
    response.set_cookie(
        key="token",
        value=access_token,
        expires=jwt_settings.token_expires * 60,
        domain=jwt_settings.url_base,
        httponly=True,
        secure=True,
    )
    return response


@router.get("/logout")
async def route_logout_and_remove_cookie(
    jwt_settings: Annotated[JwtSettings, Depends(get_jwt_settings)],
):
    response = RedirectResponse(url="", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="token", domain=jwt_settings.url_base)
    return response


@router.get("/authenticated", response_model=UserBase)
def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/forgot/password", response_model=UserBase)
async def forgot_password(req: Request):
    body = req.query_params
    email = body.get("email", None)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Must provide email"
        )

    forgotten_user = await User.get_by_email(email=email)
    if not forgotten_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
        )

    return forgotten_user


@router.get("/update/password")
def update_password(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
