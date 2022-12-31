from typing import Any, Generic, Optional, Type, TypeVar, Union

from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], collection: str):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A Pydantic BaseModel class
        * `collection`: A PyMongo ClientSession model class
        """
        self.model = model
        self.collection = collection

    async def get_all(self, session: AsyncIOMotorClient, skip: int = 0, limit: int = 20) -> dict:
        # async with session.start_transaction():
        items = await session[self.collection].find(skip=skip, limit=limit).to_list(length=limit)

        return {
            "items": [self.model(i) for i in items],
            "total": len(items)
        }

    async def get_one(self, session: AsyncIOMotorClient, model_id: Any) -> Optional[ModelType]:
        # async with session.start_transaction():
        item = await session[self.collection].find_one({"_id": ObjectId(model_id)})
        return self.model(**item)

    async def create(self, session: AsyncIOMotorClient, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        # async with session.start_transaction():
        await session.insert_one({**db_obj})
        return db_obj

    async def update(self, session: AsyncIOMotorClient, search: dict, new_key_value: dict) -> ModelType:
        # async with session.start_transaction():
        items = await session[self.collection].find_one_and_update(search, new_key_value)
        return self.model(**items)

    async def remove(self, session: AsyncIOMotorClient, model_id: Any) -> ModelType:
        # async with session.start_transaction():
        item = await session[self.collection].find_one_and_delete({"_id": ObjectId(model_id)})
        return self.model(**item)

    async def filter(self, session: AsyncIOMotorClient, column: ModelType, value: str, skip: int = 0,
                     limit: int = 20) -> dict:
        # async with session.start_transaction():
        items = await session[self.collection].find({f"{column}": value}, skip=skip, limit=limit).to_list(
            length=limit)
        return {
            "items": [self.model(**i) for i in items],
            "total": len(items)
        }

    async def aggregate(self, session: AsyncIOMotorClient, query: dict):
        # async with session.start_transaction():
        items = await session[self.collection].aggregate(query=query).to_list()
        return {
            "items": [self.model(**i) for i in items],
            "total": len(items)
        }
