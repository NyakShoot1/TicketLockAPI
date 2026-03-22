from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.domain.entity.ticker_entity import TicketStatus


class TicketCreate(BaseModel):
    reserved_by_user_id: int | None
    reserved_until: datetime | None

    event_id: int
    seat_number: int | None
    price: float
    status: TicketStatus = TicketStatus.AVAILABLE

class TicketCreateForEvent(BaseModel):
    price: Decimal

class TicketRead(TicketCreate):
    id: int

    class Config:
        from_attributes = True # todo что делает?