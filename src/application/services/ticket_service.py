import datetime

from fastapi import HTTPException

from src.core.unit_of_work import AbstractUnitOfWork
from src.domain.entity.ticker_entity import TicketEntity


class TicketService:

    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    async def reserve(self, event_id: int, ticket_id: int, user_id: int) -> TicketEntity:
        async with self._uow:
            # 1. Достаем билет с блокировкой (никто другой не сможет его забрать сейчас)
            ticket = await self._uow.tickets.find_ticket_with_lock(event_id, ticket_id)

            if not ticket:
                raise HTTPException(status_code=404, detail="Билет не найден")

            # 2. Вызываем бизнес-логику в Доменной сущности
            try:
                current_time = datetime.datetime.now(datetime.timezone.utc)
                # Метод Entity сам проверит, не занят ли билет и не оплачен ли
                ticket.reserve(user_id=user_id, current_time=current_time)
            except ValueError as e:
                # Если домен сказал "нельзя" (например, уже занято) - кидаем 400 ошибку
                raise HTTPException(status_code=400, detail=str(e))

            # 3. Сохраняем изменения
            await self._uow.tickets.update(ticket)

            # 4. Фиксируем транзакцию (в этот момент блокировка в БД снимется)
            await self._uow.commit()

            return ticket

    async def pay(self, event_id: int, ticket_id: int, user_id: int) -> TicketEntity:
        async with self._uow:
            # 1. Блокируем билет (чтобы время брони не истекло в процессе записи)
            ticket = await self._uow.tickets.find_ticket_with_lock(event_id, ticket_id)

            if not ticket:
                raise HTTPException(status_code=404, detail="Билет не найден")

            # 2. Проверяем правила оплаты в Домене
            try:
                current_time = datetime.datetime.now(datetime.timezone.utc)
                ticket.pay(user_id=user_id, current_time=current_time)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

            # 3. Имитация вызова платежного шлюза (Stripe/PayPal)
            # await self.payment_gateway.charge(...)

            # 4. Сохраняем и фиксируем
            await self._uow.tickets.update(ticket)
            await self._uow.commit()

            return ticket
