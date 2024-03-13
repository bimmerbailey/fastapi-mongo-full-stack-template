from typing import Annotated

import structlog
from fastapi import APIRouter, Security, Depends, HTTPException, status, Body

from app.dependencies.auth import get_current_user
from app.models import Item, User
from app.schemas.items import ItemUpdate

router = APIRouter(prefix="/api/v1/items", tags=["Items"])
logger = structlog.stdlib.get_logger(__name__)


@router.get("", response_model=list[Item])
async def get_items(current_user: Annotated[User, Security(get_current_user)]):
    # FIXME: Pagination
    return await Item.find({}).to_list(None)


# FIXME: Actual schema
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(
    new_item: Annotated[Item, Body()],
    current_user: Annotated[User, Security(get_current_user)],
):
    return await Item(**new_item.model_dump()).save()


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: str, current_user: Annotated[User, Security(get_current_user)]
):
    db_item = await Item.get(item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return db_item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: str,
    update_data: Annotated[ItemUpdate, Body()],
    current_user: Annotated[User, Security(get_current_user)],
):
    db_item = await Item.get(item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    for k, v in update_data.model_dump(exclude_unset=True).items():
        setattr(db_item, k, v)
    await db_item.save()
    return db_item


# FIXME: Admin only
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str, current_user: Annotated[User, Security(get_current_user)]
):
    db_item = await Item.get(item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Item not found"
        )
    await db_item.delete()
