from abc import ABC, abstractmethod

from src.application.interfaces.event_repository import IEventRepository
from src.application.interfaces.ticket_repository import ITicketRepository
from src.application.interfaces.user_repository import IUserRepository

class AbstractUnitOfWork(ABC):
    # ПЕРЕЧИСЛЯЕМ ВСЕ РЕПОЗИТОРИИ ТУТ:
    tickets: ITicketRepository
    users: IUserRepository
    events: IEventRepository

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()
