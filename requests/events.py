from constants import Status

from pydantic import BaseModel, Field


class UpdateEventRequest(BaseModel):
    status: str


class EventResponse(BaseModel):
    id: int = Field(gt=0)
    status: Status
