from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from models import Bets
from requests.bets import CreateBetRequest, BetResponse, ExtendedBetResponse
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(prefix="/bets", tags=["bets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BetResponse)
async def create_bet(
    user: user_dependency, db: db_dependency, bet_request: CreateBetRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    bet_object = Bets(**bet_request.model_dump(), user_id=user.get("id"))

    db.add(bet_object)
    db.commit()

    return bet_object


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[ExtendedBetResponse]
)
async def get_bets(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    bets_objects = db.query(Bets).filter(Bets.user_id == user.get("id")).all()

    return bets_objects
