from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from sqlalchemy.orm import selectinload

from src.user import schemas, models
from src.database import get_async_session, async_sessionmaker
from src.user.models import User
from src.user.schemas import UserCreate, UserRead as UserSchema, UserUpdate
from passlib.context import CryptContext
from .base_config import current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/create_user", response_model=UserSchema)
async def create_user(user: Annotated[UserCreate, Depends()], db: AsyncSession = Depends(get_async_session)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/users_all")
async def get_items():
    async with async_sessionmaker() as session:
        query = select(models.User).options(selectinload(models.User.items))
        result = await session.execute(query)
        items = result.scalars().all()
        return items


@router.get("/user/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/user/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_async_session)):
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/user/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted"}