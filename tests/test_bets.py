from fastapi import status

from main import app
from routers.events import get_db, get_current_user
from .conf import (
    override_get_db,
    override_get_current_user,
    client,
    test_bet,
    test_event,
    test_user,
)
from constants import Status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_bets(test_bet, test_user, test_event):
    response = client.get("/bets/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_create_bet(test_user, test_event):
    response = client.post("/bets/", json={"event_id": test_event.id, "amount": 10000})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == Status.NOT_PLAYED


def test_create_bet_fail(test_user, test_event):
    response = client.post("/bets/", json={"event_id": test_event.id, "amount": -10000})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
