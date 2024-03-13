from beanie import Document


class Item(Document):
    class Settings:
        name = "items"

    cost: float
    name: str
    description: str
    quantity: int
