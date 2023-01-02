from typing import Any, Optional, Union

from motor.motor_asyncio import AsyncIOMotorClient

from app.utils import hash_password, verify
from app.crud.base import CrudBase
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CrudBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, session: AsyncIOMotorClient, email: str) -> Optional[User]:
        one_user = await session["users"].find_one({"email": email})
        if not one_user:
            return None
        return self.model(**one_user)

    async def get_users(self, session: AsyncIOMotorClient, skip: int = 0, limit: int = 20) -> Optional[list[User]]:
        users = await session["users"].find({}, skip=skip, limit=limit).to_list(length=limit)
        return [self.model(**i) for i in users]

    async def create(self, session: AsyncIOMotorClient, obj_in: UserCreate) -> Optional[User]:
        db_obj = User(
            email=obj_in.email,
            password=hash_password(obj_in.password),
            is_admin=obj_in.is_admin
        )
        await session["users"].insert_one(db_obj.__dict__)
        return db_obj

    async def authenticate(self, session: AsyncIOMotorClient, email: str, password: str) -> Optional[User]:
        user_auth = await self.get_by_email(session, email=email)
        if not user_auth:
            return None
        if not verify(password, user_auth.password):
            return None
        return user_auth

    @property
    def is_active(self) -> bool:
        return user.is_active

    @property
    def is_admin(self) -> bool:
        return user.is_admin


user = CRUDUser(model=User, collection="users")
