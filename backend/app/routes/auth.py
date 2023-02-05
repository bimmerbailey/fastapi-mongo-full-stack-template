from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from motor.core import AgnosticDatabase
from starlette.responses import RedirectResponse

from app.models.users import User
from app.database.init_db import get_db
from app.schemas.users import Token, UserBase
from app import oauth, utils
from app.config.config import settings
from app.crud.users import user
from app.config.logging import logger

router = APIRouter(tags=['Authentication'], prefix='/api/v1')


@router.post('/login', response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AgnosticDatabase = Depends(get_db)):
    auth_user = await user.get_by_email(db, user_credentials.username)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, auth_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    access_token = oauth.create_access_token(data={"user_id": str(auth_user.id)})

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer", "is_admin": auth_user.is_admin})
    response.set_cookie(key="token", value=access_token,
                        expires=settings.access_token_expire_minutes * 60,
                        domain=settings.url_base, httponly=True, secure=True)
    return response


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="token", domain=settings.url_base)
    return response


@router.get("/authenticated", response_model=UserBase)
def read_user_me(db: AgnosticDatabase = Depends(get_db),
                 current_user: User = Depends(oauth.get_current_user),
                 ):
    return current_user


@router.get("/forgot/password", response_model=UserBase)
def forgot_password(req: Request, db: AgnosticDatabase = Depends(get_db)):
    body = req.query_params
    email = body.get("email", None)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Must give email")

    forgotten_user = user.get_by_email(db=db, email=email)
    if not forgotten_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"User not found")

    return forgotten_user.__dict__
