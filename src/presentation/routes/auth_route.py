from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.application.services.user_service import UserService
from src.core.security import verify_password, create_access_token
from src.core.unit_of_work import AbstractUnitOfWork
from src.presentation.dependencies import get_uow, get_user_service
from src.presentation.schemas.user_schemas import UserRead, UserCreate

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserRead)
async def register_user(
        data: UserCreate,
        service: UserService = Depends(get_user_service)
):
    """Регистрация нового пользователя"""
    return await service.register_user(data)

@auth_router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        uow: AbstractUnitOfWork = Depends(get_uow)
):
    async with uow:
        user = await uow.users.find_by_email(form_data.username)
        # Проверка пароля (через bcrypt)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Выпуск токена
        token = create_access_token(data={
            "sub": str(user.email),
            "role": user.role,
            "user_id": user.id
        })

        return {"access_token": token, "token_type": "bearer"}