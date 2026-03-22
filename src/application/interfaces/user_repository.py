from abc import abstractmethod

from src.core.base_repository import BaseRepository
from src.domain.entity.user_entity import UserEntity


class IUserRepository(BaseRepository[UserEntity]):

    @abstractmethod
    async def find_by_email(self, email: str) -> UserEntity | None:
        pass
