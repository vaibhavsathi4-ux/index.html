import os
from typing import AsyncGenerator
from fastapi import Header, HTTPException, Depends
from .config import settings
from .auth import verify_token
from .cache import get_context, push_context, delete_context
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# DB
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_user_id(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = authorization.split(" ", 1)[1]
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id