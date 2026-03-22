from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from src.application.services.event_service import EventService
from src.application.services.ticket_service import TicketService
from src.application.services.user_service import UserService
from src.core.security import decode_access_token
from src.core.unit_of_work import AbstractUnitOfWork
from src.domain.entity.user_entity import UserEntity, UserRole
from src.infrastructure.sqlalchemy.session import async_session
from src.infrastructure.sqlalchemy.uow import SqlAlchemyUnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_sql_alchemy_uow() -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=async_session)

def get_uow() -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=async_session)

async def get_ticket_service(uow: AbstractUnitOfWork = Depends(get_uow)) -> TicketService:
    return TicketService(uow)


async def get_user_service(uow: AbstractUnitOfWork = Depends(get_uow)) -> UserService:
    return UserService(uow)


async def get_event_service(uow: AbstractUnitOfWork = Depends(get_uow)) -> EventService:
    return EventService(uow)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        uow: AbstractUnitOfWork = Depends(get_uow)
) -> UserEntity:
    """
    Зависимость, которая проверяет JWT и возвращает объект UserEntity.
    """
    # 1. Декодируем токен (используя наш публичный ключ)
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Достаем email из поля 'sub' (мы его туда клали при логине)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Токен не содержит информации о пользователе")

    # 3. Ищем пользователя в базе
    async with uow:
        user = await uow.users.find_by_email(email)
        if user is None:
            raise HTTPException(status_code=401, detail="Пользователь не найден")

        # Возвращаем сущность. Теперь она будет доступна в роутере!
        return user

def admin_required(current_user: UserEntity = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для администраторов"
        )
    return current_user