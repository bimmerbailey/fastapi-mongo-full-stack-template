from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase, AgnosticCollection
import structlog

from app.config.config import settings
from app.models.users import Users

logger: structlog.stdlib.BoundLogger = structlog.getLogger(__name__)


class DataBase:
    client: AsyncIOMotorClient = None

    def get_db(self) -> AgnosticDatabase | None:
        if self.client:
            return self.client[settings.database_name]
        else:
            return None

    def get_collection(
        self, collection_name: str
    ) -> AgnosticCollection | None:
        db = self.get_db()
        if db:
            return db[collection_name]
        else:
            return None


db_client = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db_client.client


async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    db_client.client = AsyncIOMotorClient(
        settings.database_url, maxPoolSize=10, minPoolSize=10
    )
    # Initialize beanie
    await init_beanie(database=db_client.get_db(), document_models=[Users])
    logger.info("Connected to MongoDB!")


async def close_mongo_connection():
    logger.info("Closing connection to MongoDB...")
    db_client.client.close()
    logger.info("Connection closed!")
