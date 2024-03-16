import asyncio
from datetime import datetime, timezone

import faker
import structlog

from app.dependencies.auth import get_crypt_context
from app.dependencies.database import close_mongo_connection, connect_to_mongo
from app.models import User, Item

logger = structlog.stdlib.get_logger("development.populate")


async def create_users(crypt_context=get_crypt_context()):
    logger.info("Dropping local Users collection")
    await User.delete_all()

    users = [
        User(
            **{
                "email": "admin@your-app.com",
                "first_name": "admin",
                "password": crypt_context.hash("password"),
                "created_date": datetime.now(tz=timezone.utc),
                "is_admin": True,
            }
        ),
        User(
            **{
                "email": "user@your-app.com",
                "first_name": "user",
                "password": crypt_context.hash("password"),
                "created_date": datetime.now(tz=timezone.utc),
            }
        ),
    ]

    await User.insert_many(users)
    logger.info("Users added")


async def create_items(item_count=50):
    fake = faker.Faker()
    logger.info("Dropping Item collection")
    await Item.delete_all()
    for _ in range(item_count):
        await Item(
            name=fake.word(),
            description=fake.sentence(),
            cost=fake.pyfloat(),
            quantity=fake.pyint(0, 100),
        ).save()


async def create_dev_data():
    client = await connect_to_mongo()
    await create_users()
    await create_items()
    await close_mongo_connection(client)


if __name__ == "__main__":
    asyncio.run(create_dev_data())
