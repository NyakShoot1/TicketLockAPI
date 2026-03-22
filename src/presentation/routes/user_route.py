from fastapi import APIRouter, Depends

from src.application.services.user_service import UserService
from src.domain.entity.user_entity import UserRole
from src.presentation.dependencies import get_user_service, admin_required
from src.presentation.schemas.user_schemas import UserRead, UserCreate

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.post("/set_role/{user_id}", response_model=UserRead)
async def set_user_role(
        user_id: int,
        user_role: UserRole,
        _=Depends(admin_required),
        service: UserService = Depends(get_user_service)
):
    return await service.set_user_role(user_id, user_role)
