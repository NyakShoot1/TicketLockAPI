from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.infrastructure.sqlalchemy.base_model import Base
from src.infrastructure.sqlalchemy.models.user_model import UserModel
from src.infrastructure.sqlalchemy.models.event_model import EventModel
from src.infrastructure.sqlalchemy.models.ticket_model import TicketModel

from src.infrastructure.sqlalchemy.session import engine
from src.presentation import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="SubTracker", lifespan=lifespan)

app.include_router(api_v1_router)


@app.get("/")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
