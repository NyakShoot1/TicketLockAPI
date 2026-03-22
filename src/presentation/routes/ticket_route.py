from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks

from src.application.services.ticket_service import TicketService
from src.domain.entity.user_entity import UserEntity
from src.presentation.dependencies import get_ticket_service, get_current_user
from src.presentation.schemas.ticket_schemas import TicketRead

ticket_router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@ticket_router.post("/{ticket_id}/reserve", response_model=Optional[TicketRead])
async def create_ticket_reservation(
        ticket_id: int,
        event_id: int,
        current_user: UserEntity = Depends(get_current_user),
        ticket_service: TicketService = Depends(get_ticket_service),
):
    return await ticket_service.reserve(event_id, ticket_id, current_user.id)


@ticket_router.post("/{ticket_id}/pay", response_model=TicketRead)
async def pay_for_ticket(
        event_id: int,
        ticket_id: int,
        current_user: UserEntity = Depends(get_current_user),
        service: TicketService = Depends(get_ticket_service)
):
    """Оплата забронированного билета"""
    return await service.pay(event_id, ticket_id, current_user.id)
