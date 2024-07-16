from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from typing import Annotated, List

from src.database import get_async_session
from src.posts.models import Post
from src.posts.schemas import PostCreate, PostRead
from src.user.models import User
from ..user.base_config import current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

MAX_PAYLOAD_SIZE = 1 * 1024 * 1024


@router.post("/", response_model=PostRead)
async def create_post(
    request: Request,
    post: Annotated[PostCreate, Depends()],
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    content_length = request.headers.get('content-length')
    if content_length and int(content_length) > MAX_PAYLOAD_SIZE:
        raise HTTPException(status_code=413, detail="Payload too large")

    db_post = Post(text=post.text, owner_id=current_user.id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[PostRead])
@cache(expire=300)
async def get_posts(db: AsyncSession = Depends(get_async_session), current_user: User = Depends(current_user)):
    query = select(Post).filter(Post.owner_id == current_user.id)
    result = await db.execute(query)
    posts = result.scalars().all()
    return posts


@router.delete("/{post_id}")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_async_session),
                      current_user: User = Depends(current_user)):
    query = select(Post).filter(Post.id == post_id, Post.owner_id == current_user.id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(post)
    await db.commit()
