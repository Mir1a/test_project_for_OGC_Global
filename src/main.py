import os

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy.orm import Session


from .database import async_sessionmaker
from src.user.routers import router as user_router
from .posts.routers import router as posts_router
from .user.base_config import fastapi_users, auth_backend, current_user
from .user.schemas import UserRead, UserCreate
from .user import models
import logging
from fastapi import FastAPI
from redis import asyncio as aioredis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Test_app"
)


def get_db():
    db = async_sessionmaker()
    try:
        yield db
    finally:
        db.close()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(user_router)
app.include_router(posts_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)