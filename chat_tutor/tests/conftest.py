import os
import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from sqlalchemy.pool import NullPool

from app.main import app
from app.models import Base
from app.dependencies import get_db

# ---------------------------------------------------------------------
# Test Environment
# ---------------------------------------------------------------------

DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite+aiosqlite:///./test.db"
)

os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["JWT_SECRET"] = "test-secret"

# ---------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ---------------------------------------------------------------------
# Event Loop
# ---------------------------------------------------------------------

@pytest.fixture(scope="session")
def event_loop():

    loop = asyncio.new_event_loop()

    yield loop

    loop.close()

# ---------------------------------------------------------------------
# Create Tables
# ---------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)

# ---------------------------------------------------------------------
# Database Dependency Override
# ---------------------------------------------------------------------

async def override_get_db():

    async with TestingSessionLocal() as session:

        yield session

app.dependency_overrides[get_db] = override_get_db

# ---------------------------------------------------------------------
# Database Fixture
# ---------------------------------------------------------------------

@pytest.fixture()
async def db() -> AsyncGenerator[AsyncSession, None]:

    async with TestingSessionLocal() as session:

        yield session

# ---------------------------------------------------------------------
# HTTP Client
# ---------------------------------------------------------------------

@pytest.fixture()
async def client():

    async with AsyncClient(
        app=app,
        base_url="http://testserver",
    ) as client:

        yield client

# ---------------------------------------------------------------------
# Authorization Header
# ---------------------------------------------------------------------

@pytest.fixture()
def auth_headers():

    from jose import jwt

    token = jwt.encode(
        {
            "sub": "test-user"
        },
        "test-secret",
        algorithm="HS256",
    )

    return {

        "Authorization": f"Bearer {token}"

    }

# ---------------------------------------------------------------------
# Sample User
# ---------------------------------------------------------------------

@pytest.fixture()
def sample_user():

    return {

        "id": "test-user",

        "email": "test@example.com",

        "name": "Test User"

    }

# ---------------------------------------------------------------------
# Sample Ask Payload
# ---------------------------------------------------------------------

@pytest.fixture()
def ask_payload():

    return {

        "user_id": "test-user",

        "subject": "python",

        "message": "Explain decorators.",

        "history": []

    }