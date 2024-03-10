from datetime import datetime, timezone
from typing import Optional

import pymongo
from beanie import Document
from pydantic import EmailStr


class User(Document):
    created_date: datetime = datetime.now(tz=timezone.utc)
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str
    is_admin: bool = False

    class Settings:
        name = "users"
        indexes = [[("email", pymongo.TEXT)]]

    @classmethod
    async def get_by_email(cls, email: str) -> Optional["User"]:
        return await cls.find_one({"email": email})
