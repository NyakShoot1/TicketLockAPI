from typing import Any, Self

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @classmethod
    def from_entity(cls, entity: Any) -> Self:
        raise NotImplementedError("Метод from_entity должен быть переопределен")
