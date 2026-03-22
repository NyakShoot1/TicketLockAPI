from abc import abstractmethod

from src.core.base_repository import BaseRepository
from src.domain.entity.ticker_entity import TicketEntity


class ITicketRepository(BaseRepository[TicketEntity]):

    @abstractmethod
    async def create_bulk(self, tickets: list[TicketEntity]) -> None:
        """Массовая вставка билетов"""
        raise NotImplementedError()

    @abstractmethod
    async def find_tickets_by_event_id(self, event_id: int, limit: int, offset: int) -> list[TicketEntity]:
        """Получить все билеты по айди евента"""
        raise NotImplementedError()

    @abstractmethod
    async def find_ticket_by_event_id(self, event_id: int, ticket_id: int) -> TicketEntity:
        """Получить билет по айди ивента и самого айди билета"""
        raise NotImplementedError()

    @abstractmethod
    async def find_ticket_with_lock(self, event_id: int, ticket_id: int) -> TicketEntity | None:
        """Блокирует все изменения с билетом на время поиска"""
        raise NotImplementedError()