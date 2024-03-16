import structlog
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import DatabaseSettings, get_db_settings
from app.models import User, Item

logger = structlog.stdlib.get_logger(__name__)


async def connect_to_mongo(
    settings: DatabaseSettings = get_db_settings(),
) -> AsyncIOMotorClient:
    logger.info("Connecting to MongoDB...")
    kwargs = {
        "username": settings.username,
        "password": settings.password.get_secret_value(),
    }
    client = AsyncIOMotorClient(str(settings.database_url), **kwargs)
    await init_beanie(database=client[settings.name], document_models=[User, Item])
    logger.info("Connected to MongoDB!")
    return client


async def close_mongo_connection(client: AsyncIOMotorClient):
    logger.info("Closing connection to MongoDB...")
    client.close()
    logger.info("Connection closed!")
