from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ManyItems(BaseModel):
    items: list[T]
    total: int
