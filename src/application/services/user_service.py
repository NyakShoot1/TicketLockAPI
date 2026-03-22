from fastapi import HTTPException

from src.core.security import hash_password
from src.core.unit_of_work import AbstractUnitOfWork
from src.domain.entity.user_entity import UserEntity, UserRole
from src.presentation.schemas.user_schemas import UserCreate


class UserService:

    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    async def register_user(self, data: UserCreate) -> UserEntity:
        async with self._uow:
            # 1. Проверяем, не занят ли email
            existing_user = await self._uow.users.find_by_email(str(data.email))
            if existing_user:
                raise HTTPException(status_code=400, detail="User with this email already exists")

            # 2. Хэшируем пароль
            hashed_pw = hash_password(data.password)

            # 3. Создаем сущность
            new_user = UserEntity(
                id=None,
                email=str(data.email),
                hashed_password=hashed_pw
            )

            # 4. Сохраняем
            saved_user = await self._uow.users.create(new_user)
            await self._uow.commit()
            return saved_user

    async def set_user_role(self, user_id: int, user_role: UserRole) -> UserEntity:
        async with self._uow:
            existing_user : UserEntity = await self._uow.users.find_by_id(user_id)

            if not existing_user:
                raise HTTPException(
                    status_code=404,
                    detail=f"User with ID {user_id} not found"
                )

            existing_user.set_role(user_role)

            updated_user = await self._uow.users.update(existing_user)

            await self._uow.commit()
            return updated_user