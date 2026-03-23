from typing import Sequence

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.ticket_repository import ITicketRepository
from src.domain.entity.ticker_entity import TicketEntity
from src.infrastructure.sqlalchemy.models.ticket_model import TicketModel


class SqlAlchemyTicketRepositoryImpl(ITicketRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_ticket_with_lock(self, event_id: int, ticket_id: int) -> TicketEntity | None:
        stmt = (
            select(TicketModel)
            .where(TicketModel.event_id == event_id)
            .where(TicketModel.id == ticket_id)
            .with_for_update()  # ЭТА СТРОЧКА ЗАПРЕЩАЕТ DOUBLE BOOKING
        )
        result = await self.session.execute(stmt)
        db_ticket = result.scalar_one_or_none()

        return db_ticket.to_entity() if db_ticket else None

    async def find_tickets_by_event_id(self, event_id: int, limit: int = 10, offset: int = 0) -> list[TicketEntity]:
        stmt = (
            select(TicketModel)
            .where(TicketModel.event_id == event_id)
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(stmt)
        db_tickets = result.scalars().all()

        return [t.to_entity() for t in db_tickets]

    async def find_ticket_by_event_id(self, event_id: int, ticket_id: int) -> TicketEntity:
        stmt = (
            select(TicketModel)
            .where(TicketModel.event_id == event_id)
            .where(TicketModel.id == ticket_id)
        )

        result = await self.session.execute(stmt)

        db_ticket = result.scalars().first()

        return db_ticket.to_entity()

    async def create(self, entity: TicketEntity) -> TicketEntity:
        pass

    async def create_bulk(self, tickets: list[TicketEntity]) -> None:
        """Массовая вставка билетов"""
        if not tickets:
            return

        # 1. Превращаем список Доменных сущностей в список словарей (dict)
        # Это нужно, чтобы SQLAlchemy сгенерировала один гигантский SQL-запрос
        ticket_dicts = [
            {
                "event_id": t.event_id,
                "seat_number": t.seat_number,
                "price": t.price,
                # Если status это Enum, нужно передать его текстовое значение:
                "status": t.status.value if hasattr(t.status, 'value') else t.status,
                "reserved_by_user_id": None,
                "reserved_until": None
            }
            for t in tickets
        ]

        # 2. ВЫПОЛНЯЕМ
        await self.session.execute(insert(TicketModel), ticket_dicts)

    async def findall(self) -> Sequence[TicketEntity]:
        pass

    async def find_by_id(self, id_: int) -> TicketEntity | None:
        pass

    async def update(self, entity: TicketEntity) -> TicketEntity:
        """Обновление билета (статус, время брони, id юзера)"""
        db_ticket = await self.session.merge(TicketModel.from_entity(entity))
        await self.session.flush()
        return entity

    async def delete_by_id(self, id_: int) -> TicketEntity:
        pass
