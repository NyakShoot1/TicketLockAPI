import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.event_repository import IEventRepository
from src.domain.entity.event_entity import EventEntity
from src.infrastructure.sqlalchemy.models.event_model import EventModel


class SqlAlchemyEventRepositoryImpl(IEventRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: EventEntity) -> EventEntity:
        db_event = EventModel.from_entity(entity)

        self.session.add(db_event)
        await self.session.flush()
        await self.session.refresh(db_event)

        entity.id = db_event.id
        return entity

    async def find_upcoming(self) -> list[EventEntity]:
        # Получаем только те события, которые еще не прошли
        now = datetime.datetime.now(datetime.timezone.utc)
        stmt = select(EventModel).where(EventModel.event_date >= now).order_by(EventModel.event_date)
        result = await self.session.execute(stmt)
        return [e.to_entity() for e in result.scalars().all()]

    async def find_by_id(self, id_: int) -> EventEntity | None:
        db_event: EventModel | None = await self.session.get(EventModel, id_)

        if not db_event:
            return None

        return db_event.to_entity()

    async def findall(self) -> Sequence[EventEntity]:
        result = await self.session.execute(select(EventModel))
        # scalars() извлекает сами объекты моделей, а не кортежи
        db_events = result.scalars().all()

        return [e.to_entity() for e in db_events]

    async def update(self, entity: EventEntity) -> EventEntity:
        # merge автоматически находит запись по ID и обновляет её
        db_event = await self.session.merge(EventModel.from_entity(entity))
        await self.session.flush()
        return entity

    async def delete_by_id(self, id_: int) -> EventEntity:
        # 1. Сначала находим объект, чтобы вернуть его согласно интерфейсу
        db_event : EventModel | None = await self.session.get(EventModel, id_)

        if not db_event:
            raise ValueError(f"Мероприятие с id {id_} не найдено")

        # 2. Мапим в Entity перед удалением
        entity = db_event.to_entity()

        # 3. Удаляем из сессии (без await, это пометка)
        await self.session.delete(db_event)
        # flush отправит DELETE в базу
        await self.session.flush()

        return entity
