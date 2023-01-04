from pydantic import BaseModel


class ManyItems(BaseModel):
    items: list
    total: int
