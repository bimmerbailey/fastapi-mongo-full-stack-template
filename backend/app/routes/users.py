from typing import List

import structlog
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, HTTPException, status

from app.crud.users import user
from app.schemas.users import UserCreate, UserOut

router = APIRouter(prefix="/api/v1/users", tags=["Users"])
logger: structlog.stdlib.BoundLogger = structlog.getLogger(__name__)


@router.get("", response_model=List[UserOut])
async def get_users():
    return await user.get_users()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(new_user: UserCreate):
    try:
        valid = validate_email(new_user.email, check_deliverability=False)
        email = valid.normalized
    except EmailNotValidError as e:
        logger.warning("Email Error", e=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    db_user = await user.get_by_email(email)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user.create(new_user)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    db_user = await user.get_one(user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user
