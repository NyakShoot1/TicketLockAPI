from fastapi import APIRouter, Depends

from src.application.services.event_service import EventService
from src.presentation.dependencies import get_event_service, get_current_user, admin_required
from src.presentation.schemas.event_schemas import EventRead, EventCreate
from src.presentation.schemas.ticket_schemas import TicketCreateForEvent, TicketRead

event_router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@event_router.post("/create", response_model=EventRead)
async def create_event(
        event_data: EventCreate,
        ticket_data: TicketCreateForEvent,
        _ = Depends(admin_required),
        event_service: EventService = Depends(get_event_service),
):
    return await event_service.create_event_with_tickets(event_data=event_data, ticket_data=ticket_data)


@event_router.get("/{event_id}/tickets", response_model=list[TicketRead])
async def get_event_tickets(
        event_id: int,
        limit: int = 10,  # По умолчанию 10 билетов
        offset: int = 0,  # Начинаем с самого первого
        _ = Depends(get_current_user),
        event_service: EventService = Depends(get_event_service),
):
    return await event_service.get_event_tickets(event_id=event_id, limit=limit, offset=offset)


@event_router.get("/", response_model=list[EventRead])
async def get_upcoming_events(
        event_service: EventService = Depends(get_event_service),
):
    """Получить список всех будущих мероприятий"""
    return await event_service.get_upcoming_events()
