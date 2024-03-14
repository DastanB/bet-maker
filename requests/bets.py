from pydantic import BaseModel, Field
from decimal import Decimal
from constants import Status


class CreateBetRequest(BaseModel):
    event_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class BetResponse(BaseModel):
    id: int = Field(gt=0)
    status: Status


class ExtendedBetResponse(BetResponse):
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    event_id: int = Field(gt=0)
