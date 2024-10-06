import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncIterator

from main import app
from app.models import Base
from app.settings import database_settings


# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/test_database"
# SYNC_DATABASE_URL = "postgresql://postgres:postgres@db:5432/test_database"

async_engine = create_async_engine(database_settings.test_url, echo=True, poolclass=NullPool)

TestSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
def create_and_drop_test_database():
    sync_engine = create_engine(database_settings.test_sync_url)
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)
    yield
    drop_database(sync_engine.url)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_test_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncIterator[AsyncSession]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
def cat_payload():
    return {
        "name": "Whiskers",
        "color": "Black",
        "age": 12,
        "description": "A friendly cat",
        "breed": "Siamese",
    }
