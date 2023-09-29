import structlog
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.config import settings
from app.models.users import Users

logger = structlog.stdlib.get_logger(__name__)


async def connect_to_mongo() -> AsyncIOMotorClient:
    logger.info("Connecting to MongoDB...")
    kwargs = {
        "username": settings.database_username,
        "password": settings.database_password,
    }
    client = AsyncIOMotorClient(str(settings.database_url), **kwargs)
    await init_beanie(database=client[settings.database_name], document_models=[Users])
    logger.info("Connected to MongoDB!")
    return client


async def close_mongo_connection(client: AsyncIOMotorClient):
    logger.info("Closing connection to MongoDB...")
    client.close()
    logger.info("Connection closed!")
