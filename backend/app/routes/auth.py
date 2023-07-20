from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
import structlog

from app.models.users import Users
from app.schemas.users import Token, UserBase
from app import oauth, utils
from app.config.config import settings
from app.crud.users import user
from app.oauth import get_current_user


router = APIRouter(tags=["Authentication"], prefix="/api/v1")
logger: structlog.stdlib.BoundLogger = structlog.getLogger(__name__)


@router.post("/login", response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    auth_user = await user.get_by_email(user_credentials.username)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Credentials",
        )

    if not utils.verify(user_credentials.password, auth_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Credentials",
        )

    access_token = oauth.create_access_token(
        data={"user_id": str(auth_user.id)}
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
        expires=settings.access_token_expire_minutes * 60,
        domain=settings.url_base,
        httponly=True,
        secure=True,
    )
    return response


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="token", domain=settings.url_base)
    return response


@router.get("/authenticated", response_model=UserBase)
def read_user_me(current_user: Users = Depends(oauth.get_current_user)):
    return current_user


@router.get("/forgot/password", response_model=UserBase)
def forgot_password(req: Request):
    body = req.query_params
    email = body.get("email", None)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Must give email"
        )

    forgotten_user = user.get_by_email(email=email)
    if not forgotten_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"User not found"
        )

    return forgotten_user.__dict__


@router.get("/update/password")
def update_password(current_user: Users = Depends(get_current_user)):
    pass