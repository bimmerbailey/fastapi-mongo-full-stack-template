from typing import Annotated

import structlog
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Security, Depends, HTTPException, status

from app.dependencies.auth import CryptContext, get_crypt_context, get_current_user
from app.models.users import User
from app.schemas.users import UserCreate, UserOut

router = APIRouter(
    prefix="/api/v1/users", tags=["Users"], dependencies=[Security(get_current_user)]
)
logger: structlog.stdlib.BoundLogger = structlog.getLogger(__name__)


@router.get("", response_model=list[UserOut])
async def get_users():
    # FIXME: Pagination
    return await User.find({}).to_list(None)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    new_user: UserCreate,
    crypt_context: Annotated[CryptContext, Depends(get_crypt_context)],
):
    try:
        valid = validate_email(new_user.email, check_deliverability=False)
        email = valid.normalized
    except EmailNotValidError as e:
        logger.warning("Email Error", e=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    db_user = await User.get_by_email(email)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user.password = crypt_context.hash(new_user.password)
    return await User(**new_user.dict()).save()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    db_user = await User.get(user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user
