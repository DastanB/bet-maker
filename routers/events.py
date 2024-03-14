from typing import Annotated

from fastapi import APIRouter, Path, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from constants import Status
from models import Events, Bets
from requests.events import UpdateEventRequest, EventResponse
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(prefix="/events", tags=["events"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
async def create_event(db: db_dependency):
    event_object = Events(status=Status.NOT_PLAYED)

    db.add(event_object)
    db.commit()

    return event_object


@router.put("/{event_id}", status_code=status.HTTP_200_OK, response_model=EventResponse)
async def update_event(
    db: db_dependency, event_request: UpdateEventRequest, event_id: int = Path(gt=0)
):
    event_object = db.query(Events).filter(Events.id == event_id).first()

    if event_object.status != Status.NOT_PLAYED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Event already updated."
        )

    event_object.status = event_request.status

    db.add(event_object)

    update_data = [
        {"id": bet_object.id, "status": event_request.status}
        for bet_object in db.query(Bets).filter(Bets.event_id == event_id).all()
    ]

    db.bulk_update_mappings(Bets, update_data)
    db.commit()

    return event_object
