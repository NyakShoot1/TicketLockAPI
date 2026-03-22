from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class EventCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100, examples=["Stand Up Show"])
    location: str = Field(min_length=3, max_length=200, examples=["Madison Square Garden"])
    event_date: datetime

    total_tickets: int = Field(gt=0, le=100000, description="Количество мест в зале")

class EventRead(BaseModel):
    id: int
    title: str
    location: str
    event_date: datetime

    model_config = ConfigDict(from_attributes=True)