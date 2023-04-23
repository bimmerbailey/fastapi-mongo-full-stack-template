from motor.core import ClientSession

from app.utils import hash_password, verify
from app.crud.base import CrudBase
from app.models.users import Users
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CrudBase[Users, UserCreate, UserUpdate]):
    async def get_by_email(
        self, email: str, session: ClientSession | None = None
    ) -> Users:
        return await self.model.find_one(
            self.model.email == email, session=session
        )

    async def get_users(
        self,
        skip: int = 0,
        limit: int = 20,
        session: ClientSession | None = None,
    ) -> list[Users] | None:
        return (
            await self.model.find(session=session)
            .skip(skip)
            .limit(limit)
            .to_list()
        )

    async def create(
        self, obj_in: UserCreate, session: ClientSession | None = None
    ) -> Users:
        db_obj = self.model(
            email=obj_in.email,
            password=hash_password(obj_in.password),
            is_admin=obj_in.is_admin,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
        )
        await db_obj.insert(session=session)
        return db_obj

    async def authenticate(
        self, email: str, password: str, session: ClientSession | None = None
    ) -> Users | None:
        user_auth = await self.get_by_email(email=email, session=session)
        if not user_auth:
            return None
        if not verify(password, user_auth.password):
            return None
        return user_auth


user = CRUDUser(model=Users)
