from typing import List

from fastapi import status, Depends, APIRouter, HTTPException
from motor.core import AgnosticDatabase

from app.schemas.users import UserOut, UserCreate
from app.database.init_db import get_db
from app.crud.users import user
from app.models.users import User
from app import oauth

router = APIRouter(
    prefix="/api/v1/users",
    tags=['Users']
)


@router.get('', response_model=List[UserOut])
async def get_users(db: AgnosticDatabase = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return await user.get_users(session=db)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(new_user: UserCreate, db: AgnosticDatabase = Depends(get_db)):
    db_user = await user.get_by_email(db, new_user.email)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user.create(db, new_user)


@router.get('/{user_id}', response_model=UserOut)
async def get_user(user_id: str, db: AgnosticDatabase = Depends(get_db)):
    db_user = await user.get_one(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user
