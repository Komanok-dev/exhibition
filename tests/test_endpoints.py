import pytest, pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterator

from main import app
from app.database import get_session
from tests.conftest import TestSessionLocal


@pytest.mark.asyncio
async def test_create_cat(async_client, cat_payload):
    async def override_get_session() -> AsyncIterator[AsyncSession]:
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    response = await async_client.post("/cats/add", json=cat_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Whiskers"
    assert data["color"] == "Black"
    assert data["age"] == 12
    assert data["description"] == "A friendly cat"
    assert data["breed"] == "Siamese"


@pytest.mark.asyncio
async def test_delete_cat(async_client, cat_payload):
    async def override_get_session() -> AsyncIterator[AsyncSession]:
        async with TestSessionLocal() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_session] = override_get_session
    create_response = await async_client.post("/cats/add", json=cat_payload)
    assert create_response.status_code == 200
    data = create_response.json()
    assert data["name"] == "Whiskers"
    cat_id = create_response.json()["id"]
    response = await async_client.delete(f"/cats/delete/{cat_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Cat deleted successfully"}


@pytest.mark.asyncio
async def test_update_cat(async_client, cat_payload):
    async def override_get_session() -> AsyncIterator[AsyncSession]:
        async with TestSessionLocal() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_session] = override_get_session
    create_response = await async_client.post("/cats/add", json=cat_payload)
    cat_id = create_response.json()["id"]
    update_payload = {"color": "White"}
    response = await async_client.put(f"/cats/update/{cat_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["color"] == "White"
