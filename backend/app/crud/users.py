from typing import Optional

from motor.core import AgnosticCollection, AgnosticClientSession

from app.utils import hash_password, verify
from app.crud.base import CrudBase
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from app.config.config import settings
from app.config.logging import logger


class CRUDUser(CrudBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, session: AgnosticClientSession, email: str) -> Optional[User]:
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        one_user = await db.find_one({"email": email}, session=session)
        if not one_user:
            return None
        return self.model(**one_user)

    async def get_users(self, session: AgnosticClientSession, skip: int = 0, limit: int = 20) -> Optional[list[User]]:
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        users = await db.find({}, skip=skip, limit=limit, session=session).to_list(length=limit)
        return [self.model(**i) for i in users]

    async def create(self, session: AgnosticClientSession, obj_in: UserCreate) -> Optional[User]:
        db_obj = User(
            email=obj_in.email,
            password=hash_password(obj_in.password),
            is_admin=obj_in.is_admin
        )
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        await db.insert_one(db_obj.__dict__, session=session)
        return db_obj

    async def authenticate(self, session: AgnosticClientSession, email: str, password: str) -> Optional[User]:
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
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
