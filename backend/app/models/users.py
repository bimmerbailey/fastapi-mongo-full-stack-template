from datetime import datetime, timezone

import pymongo
from beanie import Document
from pydantic import EmailStr


class Users(Document):
    created_date: datetime = datetime.now(tz=timezone.utc)
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str
    is_admin: bool = False

    class Settings:
        name = "users"
        indexes = [[("email", pymongo.TEXT)]]
