from typing import Optional, TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ManyItems(BaseModel):
    items: list[T]
    total: int


class BaseGet(BaseModel):
    search: Optional[str] = None
    limit: int = Query(default=20, lte=200)
    skip: int = Query(default=0, gte=0)
