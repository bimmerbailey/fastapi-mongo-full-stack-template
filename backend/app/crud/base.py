from typing import Any, Generic, Optional, Type, TypeVar, Union

from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from motor.core import AgnosticClientSession, AgnosticCollection, AgnosticClientSession
from pydantic import BaseModel

from app.config.config import settings

ModelType = TypeVar("ModelType", bound=BaseModel)
CollectionType = TypeVar("CollectionType", bound=AgnosticCollection)
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

    async def get_all(self, session: AgnosticClientSession, skip: int = 0, limit: int = 20) -> Optional[dict]:
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        items = await db.find(skip=skip, limit=limit, session=session).to_list(length=limit)
        if not items:
            return None

        return {
            "items": [self.model(i) for i in items],
            "total": len(items)
        }

    async def get_one(self, session: AgnosticClientSession, model_id: Any) -> Optional[ModelType]:
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        item = await db.find_one({"_id": ObjectId(model_id)}, session=session)
        if not item:
            return None
        return self.model(**item)

    async def create(self, session: AgnosticClientSession, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        await db.insert_one({**db_obj}, session=session)
        return db_obj

    async def update(self, session: AgnosticClientSession, search: dict, new_key_value: dict) -> Optional[ModelType]:
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        item = await db.find_one_and_update(search, new_key_value, session=session)
        if not item:
            return None
        return self.model(**item)

    async def remove(self, session: AgnosticClientSession, model_id: Any) -> Optional[ModelType]:
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        item = await db.find_one_and_delete({"_id": ObjectId(model_id)}, session=session)
        if not item:
            return None
        return self.model(**item)

    async def filter(self, session: AgnosticClientSession, column: ModelType, value: str, skip: int = 0,
                     limit: int = 20) -> Optional[dict]:
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        items = await db.find({f"{column}": value}, skip=skip, limit=limit, session=session).to_list(
            length=limit)
        if not items:
            return None
        return {
            "items": [self.model(**i) for i in items],
            "total": len(items)
        }

    async def aggregate(self, session: AgnosticClientSession, query: dict) -> Optional[dict]:
        db: AgnosticCollection = session.client[settings.database_name][self.collection]
        items = await db.aggregate(pipeline=query, session=session).to_list()
        if not items:
            return None
        return {
            "items": [self.model(**i) for i in items],
            "total": len(items)
        }
