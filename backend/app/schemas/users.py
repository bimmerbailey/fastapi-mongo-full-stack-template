from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: Optional[str] = None
    is_admin: bool = False
    first_name: str | None = None
    last_name: str | None = None


class UserOut(UserBase):
    created_date: datetime


class UserCreate(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "password": "ExAmplEpaSswOrd12",
                "is_admin": False,
            }
        }


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: Optional[bool]


class TokenData(BaseModel):
    id: Optional[str] = None
