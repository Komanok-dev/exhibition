from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncIterator
from typing_extensions import Annotated

from app.settings import database_settings

async_engine: AsyncEngine = create_async_engine(database_settings.url, echo=True)


def get_async_sessionmaker():
    return sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async_sessionmaker = get_async_sessionmaker()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_sessionmaker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        else:
            await session.commit()
        finally:
            await session.close()


DatabaseSession = Annotated[AsyncSession, Depends(get_session)]
