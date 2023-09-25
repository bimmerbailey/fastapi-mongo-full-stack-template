import asyncio
from datetime import datetime, timezone

import structlog
from beanie import init_beanie
from config.config import settings
from models.users import Users
from motor.motor_asyncio import AsyncIOMotorClient
from utils import hash_password

logger: structlog.stdlib.BoundLogger = structlog.getLogger(__name__)


async def connect_db():
    db_client = AsyncIOMotorClient(
        settings.database_url, maxPoolSize=10, minPoolSize=10
    )
    await init_beanie(db_client[settings.database_name], document_models=[Users])


async def create_users():
    logger.info("Dropping local Users collection")
    await Users.delete_all()

    users = [
        Users(
            **{
                "email": "admin@your-app.com",
                "first_name": "admin",
                "password": hash_password("password"),
                "created_date": datetime.now(tz=timezone.utc),
                "is_admin": True,
            }
        ),
        Users(
            **{
                "email": "user@your-app.com",
                "first_name": "user",
                "password": hash_password("password"),
                "created_date": datetime.now(tz=timezone.utc),
            }
        ),
    ]

    await Users.insert_many(users)
    logger.info("Users added")


async def create_dev_data():
    await connect_db()
    await create_users()


if __name__ == "__main__":
    asyncio.run(create_dev_data())
