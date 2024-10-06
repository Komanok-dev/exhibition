from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import DatabaseSession
from app.models import Cat, Breed
from app.schemas import CatResponse, BreedResponse, CatCreate, CatUpdate

router = APIRouter(tags=["Cats"], prefix="/cats")


def create_cat_response(cat: Cat, breed: Breed | None = None) -> CatResponse:
    return CatResponse(
        id=cat.id,
        name=cat.name,
        color=cat.color,
        age=cat.age,
        description=cat.description,
        breed=breed.name if breed else None,
    )


@router.get(
    "/breeds",
    description="Get list of breeds",
    response_model=list[BreedResponse],
)
async def get_breeds(session: DatabaseSession):
    return (await session.execute(select(Breed))).scalars().all()


@router.get("/", description="Get list of cats", response_model=list[CatResponse])
async def get_cats(session: DatabaseSession, breed: str | None = None):
    query = select(Cat).options(joinedload(Cat.breed))
    if breed:
        query = query.join(Cat.breed).where(Breed.name == breed.title())
    cats = (await session.execute(query)).scalars().all()
    return [
        CatResponse(
            id=cat.id,
            name=cat.name,
            color=cat.color,
            age=cat.age,
            description=cat.description,
            breed=cat.breed.name,
        )
        for cat in cats
    ]


@router.get("/{cat_id}", description="Get cat by id", response_model=CatResponse)
async def get_cat_by_id(cat_id: int, session: DatabaseSession):
    cat = (
        await session.execute(
            select(Cat).where(Cat.id == cat_id).options(joinedload(Cat.breed))
        )
    ).scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return create_cat_response(cat)


@router.post("/add", description="Add cat", response_model=CatResponse)
async def add_cat(new_cat: CatCreate, session: DatabaseSession):
    breed = None
    if new_cat.breed:
        breed_result = await session.execute(
            select(Breed).where(Breed.name.ilike(new_cat.breed))
        )
        breed = breed_result.scalar_one_or_none()
        if not breed:
            breed = Breed(name=new_cat.breed.title())
            session.add(breed)
            await session.flush()

    cat = Cat(
        name=new_cat.name,
        color=new_cat.color,
        age=new_cat.age,
        description=new_cat.description,
        breed_id=breed.id if breed else None,
    )
    session.add(cat)
    await session.flush()
    return create_cat_response(cat, breed)


@router.put("/update/{cat_id}", description="Update cat", response_model=CatResponse)
async def update_cat(cat_id: int, new_cat: CatUpdate, session: DatabaseSession):
    breed = None
    result = await session.execute(select(Cat).where(Cat.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    if new_cat.breed:
        breed_result = await session.execute(
            select(Breed).where(Breed.name.ilike(new_cat.breed))
        )
        breed = breed_result.scalar_one_or_none()
        if not breed:
            breed = Breed(name=new_cat.breed.title())
            session.add(breed)
            await session.flush()
        cat.breed_id = breed.id
    update_data = new_cat.model_dump(exclude_unset=True, exclude={"breed"})
    for field, value in update_data.items():
        setattr(cat, field, value)
    return create_cat_response(cat, breed)


@router.delete("/delete/{cat_id}", description="Delete cat")
async def delete_cat(cat_id: int, session: DatabaseSession):
    result = await session.execute(select(Cat).where(Cat.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    await session.delete(cat)
    return {"message": "Cat deleted successfully"}
