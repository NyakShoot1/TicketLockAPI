from abc import abstractmethod
from typing import Sequence

from src.core.base_repository import BaseRepository
from src.domain.entity.event_entity import EventEntity


class IEventRepository(BaseRepository[EventEntity]):

    @abstractmethod
    async def find_upcoming(self) -> list[EventEntity]:
        ...
