from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entity.ticker_entity import TicketStatus, TicketEntity
from src.infrastructure.sqlalchemy.base_model import Base

if TYPE_CHECKING:
    from src.infrastructure.sqlalchemy.models.event_model import EventModel
    from src.infrastructure.sqlalchemy.models.user_model import UserModel


class TicketModel(Base):
    __tablename__ = "tickets"

    seat_number: Mapped[int]
    price: Mapped[Decimal] = mapped_column()  # todo не меньше нуля
    status: Mapped[TicketStatus] = mapped_column(default=TicketStatus.AVAILABLE)

    # Внешний ключ на таблицу events
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

    # Внешний ключ на таблицу users (nullable=True, потому что билет может быть ничьим)
    reserved_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reserved_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # ОБРАТНЫЕ СВЯЗИ (Чтобы мы могли написать ticket.event.title или ticket.user.email)
    event: Mapped["EventModel"] = relationship(back_populates="tickets")
    user: Mapped["UserModel"] = relationship(back_populates="tickets")

    @classmethod
    def from_entity(cls, entity: 'TicketEntity') -> 'TicketModel':
        return cls(
            id=entity.id,
            reserved_by_user_id=entity.reserved_by_user_id,
            reserved_until=entity.reserved_until,
            event_id=entity.event_id,
            seat_number=entity.seat_number,
            price=entity.price,
            status=entity.status,
        )

    def to_entity(self) -> TicketEntity:
        return TicketEntity(
            id=self.id,
            reserved_by_user_id=self.reserved_by_user_id,
            reserved_until=self.reserved_until,
            event_id=self.event_id,
            seat_number=self.seat_number,
            price=self.price,
            status=self.status,
        )