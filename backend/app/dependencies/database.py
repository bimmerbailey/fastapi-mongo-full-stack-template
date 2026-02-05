import structlog
from beanie import init_beanie
from pymongo.asynchronous.mongo_client import AsyncMongoClient

from app.config.settings import DatabaseSettings, get_db_settings
from app.models import Item, User

logger = structlog.stdlib.get_logger(__name__)


async def connect_to_mongo(
    settings: DatabaseSettings = get_db_settings(),
) -> AsyncMongoClient:
    logger.info("Connecting to MongoDB...")
    kwargs = {
        "username": settings.username,
        "password": settings.password.get_secret_value(),
    }
    client = AsyncMongoClient(str(settings.database_url), **kwargs)
    await init_beanie(database=client[settings.name], document_models=[User, Item])
    logger.info("Connected to MongoDB!")
    return client


async def close_mongo_connection(client: AsyncMongoClient):
    logger.info("Closing connection to MongoDB...")
    await client.close()
    logger.info("Connection closed!")
