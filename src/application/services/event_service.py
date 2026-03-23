from fastapi import HTTPException

from src.core.unit_of_work import AbstractUnitOfWork
from src.domain.entity.event_entity import EventEntity
from src.domain.entity.ticker_entity import TicketEntity, TicketStatus
from src.presentation.schemas.event_schemas import EventCreate
from src.presentation.schemas.ticket_schemas import TicketCreateForEvent


class EventService:

    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    async def create_event_with_tickets(self, event_data: EventCreate,
                                        ticket_data: TicketCreateForEvent) -> EventEntity:
        async with self._uow:
            try:
                new_event = EventEntity(
                    id=None,
                    title=event_data.title,
                    event_date=event_data.event_date,
                    location=event_data.location
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

            saved_event = await self._uow.events.create(new_event)

            tickets_to_create = [
                TicketEntity(
                    id=None,
                    event_id=saved_event.id,
                    seat_number=i,
                    price=ticket_data.price,
                    status=TicketStatus.AVAILABLE,
                    reserved_by_user_id=None,
                    reserved_until=None,
                )
                for i in range(1, event_data.total_tickets + 1)
            ]

            await self._uow.tickets.create_bulk(tickets_to_create)

            await self._uow.commit()

            return saved_event

    async def get_event_tickets(self, event_id: int, limit: int, offset: int) -> list[TicketEntity]:
        async with self._uow:
            return await self._uow.tickets.find_tickets_by_event_id(
                event_id=event_id,
                limit=limit,
                offset=offset
            )

    async def get_upcoming_events(self) -> list[EventEntity]:
        async with self._uow:
            return await self._uow.events.find_upcoming()
