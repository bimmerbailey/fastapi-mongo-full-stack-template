from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

from .base import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_date: datetime = datetime.now(tz=timezone.utc)
    email: EmailStr = Field(...)
    password: str = Field(...)
    is_admin: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "created_date": datetime.now().isoformat(),
                "password": "ExAmplEpaSswOrd12",
                "is_admin": "False",
            }
        }
