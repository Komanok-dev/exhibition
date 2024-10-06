from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import async_engine
from app.endpoints import router
from app.models import Base


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)
