from pydantic import BaseModel


class ItemUpdate(BaseModel):
    cost: float | None = None
    name: str | None = None
    description: str | None = None
    quantity: int | None = None
