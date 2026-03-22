from src.core.unit_of_work import AbstractUnitOfWork
from src.infrastructure.sqlalchemy.repository.event_repository_impl import SqlAlchemyEventRepositoryImpl
from src.infrastructure.sqlalchemy.repository.ticket_repository_impl import SqlAlchemyTicketRepositoryImpl
from src.infrastructure.sqlalchemy.repository.user_repository_impl import SqlAlchemyUserRepositoryImpl


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        # ИНИЦИАЛИЗИРУЕМ ВСЕ РЕПОЗИТОРИИ, ПЕРЕДАВАЯ ИМ ОДНУ И ТУ ЖЕ СЕССИЮ
        self.tickets = SqlAlchemyTicketRepositoryImpl(self.session)
        self.users = SqlAlchemyUserRepositoryImpl(self.session)
        self.events = SqlAlchemyEventRepositoryImpl(self.session)

        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
