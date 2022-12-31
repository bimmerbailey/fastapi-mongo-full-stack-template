from motor.motor_asyncio import AsyncIOMotorClient

from app.config.config import settings
from app.config.logging import logger

MONGODB_URL = f"mongodb://{settings.database_username}:{settings.database_password}@{settings.database_hostname}" \
              f"/{settings.database_name}?retryWrites=true&w=majority"


class DataBase:
    client: AsyncIOMotorClient = None

    def get_db(self):
        if self.client is not None:
            return self.client[settings.database_name]
        else:
            return None


database = None
db_client = DataBase()
if db_client.get_db() is not None:
    database = db_client.get_db()


async def get_database() -> AsyncIOMotorClient:
    return db_client.client


async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    db_client.client = AsyncIOMotorClient(MONGODB_URL,
                                          maxPoolSize=10,
                                          minPoolSize=10)
    logger.info("Connected to MongoDB!")


async def close_mongo_connection():
    logger.info("Closing connection to MongoDB...")
    db_client.client.close()
    logger.info("Connection closed!")


async def get_db():
    async with await db_client.client.start_session() as session:
        try:
            async with session.start_transaction():
                yield db_client.get_db()
        finally:
            session.end_session()
