from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    name: str
    password: str


class UserUpdate(schemas.BaseUser[int]):
    pass
