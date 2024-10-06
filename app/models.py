from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from typing import List, Optional

Base = declarative_base()


class Cat(Base):
    __tablename__ = "cat"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[Optional[str]]
    color: Mapped[str]
    age: Mapped[int]  # age counts in months
    description: Mapped[str]
    breed_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("breed.id"), nullable=True
    )
    breed: Mapped["Breed"] = relationship("Breed", back_populates="cats")


class Breed(Base):
    __tablename__ = "breed"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    cats: Mapped[List["Cat"]] = relationship("Cat", back_populates="breed")
