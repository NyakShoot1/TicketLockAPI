from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.user_repository import IUserRepository
from src.domain.entity.user_entity import UserEntity
from src.infrastructure.sqlalchemy.models.user_model import UserModel


class SqlAlchemyUserRepositoryImpl(IUserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_email(self, email: str) -> UserEntity | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return db_user.to_entity() if db_user else None

    async def create(self, entity: UserEntity) -> UserEntity:
        db_user = UserModel.from_entity(entity)
        self.session.add(db_user)
        await self.session.flush()
        await self.session.refresh(db_user)
        entity.id = db_user.id
        return entity

    async def findall(self) -> Sequence[UserEntity]:
        pass

    async def find_by_id(self, id_: int) -> UserEntity | None:
        db_user : UserModel | None = await self.session.get(UserModel, id_)
        return db_user.to_entity() if db_user else None

    async def update(self, entity: UserEntity) -> UserEntity:
        db_user = await self.session.merge(UserModel.from_entity(entity))
        await self.session.flush()
        return entity

    async def delete_by_id(self, id_: int) -> UserEntity:
        pass
