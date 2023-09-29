from typing import Generic, Type, TypeVar

from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from pymongo.client_session import ClientSession

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A Beanie Document class
        """
        self.model = model

    async def get_all(
        self,
        session: ClientSession | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> dict[str, ModelType | int]:
        items = await self.model.find_all(
            session=session, skip=skip, limit=limit
        ).to_list()

        return {"items": items, "total": len(items)}

    async def get_one(
        self,
        model_id: PydanticObjectId,
        session: ClientSession | None = None,
    ) -> ModelType | None:
        return await self.model.get(model_id, session=session)

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: ClientSession | None = None,
    ) -> ModelType:
        db_obj = self.model(**obj_in)
        await self.model.insert(session=session)
        return db_obj

    async def update(
        self,
        update_obj: UpdateSchemaType,
        model_id: PydanticObjectId,
        session: ClientSession | None = None,
    ) -> ModelType | None:
        item = await self.model.get(model_id, session=session)
        for key in update_obj.model_dump():
            if update_obj[key]:
                item[key] = update_obj[key]
        # NOTE: Will only update NOT create, if using save() it will create if obj doesn't exist
        await item.replace()
        return item

    async def remove(
        self,
        model_id: PydanticObjectId,
        session: ClientSession | None = None,
    ) -> ModelType | None:
        item = await self.model.get(model_id, session=session)

        return await item.delete(session=session)

    async def aggregate(self, session: ClientSession | None, pipeline: list) -> dict:
        items = await self.model.aggregate(
            aggregation_pipeline=pipeline, session=session
        )
        return {"items": [self.model(**i) for i in items], "total": len(items)}
