from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.domain.entity.event_entity import EventEntity
from src.infrastructure.sqlalchemy.base_model import Base

if TYPE_CHECKING:
    from src.infrastructure.sqlalchemy.models.ticket_model import TicketModel


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    location: Mapped[str]

    # Связь: У мероприятия есть список билетов
    # cascade="all, delete-orphan" значит, что если мы удалим концерт,
    # все его билеты тоже удалятся из БД автоматически!
    tickets: Mapped[list["TicketModel"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan"
    )

    @classmethod
    def from_entity(cls, entity: 'EventEntity') -> 'EventModel':
        return cls(
            id=entity.id,
            title=entity.title,
            event_date=entity.event_date,
            location=entity.location,
        )

    def to_entity(self) -> EventEntity:
        return EventEntity(
            id=self.id,
            title=self.title,
            event_date=self.event_date,
            location=self.location
        )