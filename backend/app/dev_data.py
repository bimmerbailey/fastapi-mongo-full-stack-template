import asyncio
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends

from app.utils import hash_password
from app.database.init_db import get_db
from app.config.config import settings


async def create_users(db: Depends(get_db)):
    await db["users"].drop()
    await db["users"].insert_one({
        "email": "admin@your-app.com",
        "password": hash_password("password"),
        "created_date": datetime.now(tz=timezone.utc),
        "is_admin": True
    })
    await db["users"].insert_one({
        "email": "user@your-app.com",
        "password": hash_password("password"),
        "created_date": datetime.now(tz=timezone.utc)
    })


if __name__ == "__main__":
    MONGODB_URL = f"mongodb://{settings.database_username}:{settings.database_password}@{settings.database_hostname}" \
                  f"/{settings.database_name}?retryWrites=true&w=majority"

    db_client = AsyncIOMotorClient(MONGODB_URL,
                                   maxPoolSize=10,
                                   minPoolSize=10)
    client_db = db_client[settings.database_name]
    asyncio.run(create_users(client_db))
