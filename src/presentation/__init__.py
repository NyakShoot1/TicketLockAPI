from fastapi import APIRouter

from src.core.settings import settings
from src.presentation.routes.auth_route import auth_router
from src.presentation.routes.event_route import event_router
from src.presentation.routes.ticket_route import ticket_router
from src.presentation.routes.user_route import user_router

api_v1_router = APIRouter(prefix=settings.api_v1_prefix)

api_v1_router.include_router(auth_router)
api_v1_router.include_router(event_router)
api_v1_router.include_router(ticket_router)
api_v1_router.include_router(user_router)