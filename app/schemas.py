from pydantic import BaseModel, Field, ConfigDict


class CatCreate(BaseModel):
    name: str | None = None
    color: str
    age: int = Field(
        ..., gt=0, description="Age of the cat, must be a positive integer"
    )
    description: str
    breed: str | None = None


class CatUpdate(BaseModel):
    name: str | None = None
    color: str | None = None
    age: int | None = Field(
        None, gt=0, description="Age of the cat, must be a positive integer"
    )
    description: str | None = None
    breed: str | None = None


class CatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str | None
    color: str
    age: int
    description: str
    breed: str | None


class BreedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
