import asyncio
import json
from sqlalchemy import insert
from app.database import get_async_sessionmaker
from app.models import Cat, Breed


with open("initial_data.json", "r") as file:
    data = json.load(file)


async def seed_database():
    async_sessionmaker = get_async_sessionmaker()
    async with async_sessionmaker() as session:
        try:
            await session.execute(insert(Breed), data["breeds"])
            await session.execute(insert(Cat), data["cats"])
            await session.commit()
            print("Data inserted successfully.")

        except Exception as e:
            await session.rollback()
            print(f"An error occurred: {e}")


asyncio.run(seed_database())
