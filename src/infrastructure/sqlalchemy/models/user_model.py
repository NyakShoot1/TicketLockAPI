from typing import TYPE_CHECKING, Self

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entity.user_entity import UserEntity, UserRole
from src.infrastructure.sqlalchemy.base_model import Base

if TYPE_CHECKING:
    from src.infrastructure.sqlalchemy.models.ticket_model import TicketModel


class UserModel(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()  # Добавь это поле в модель!
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)

    # Связь: У юзера есть список билетов, которые он забронировал
    # back_populates указывает на название переменной в связанном классе
    tickets: Mapped[list["TicketModel"]] = relationship(back_populates="user")

    @classmethod
    def from_entity(cls, entity: UserEntity) -> Self:
        return cls(
            id=entity.id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            role=entity.role
        )

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            role=self.role
        )
