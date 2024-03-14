from fastapi import status

from main import app
from routers.events import get_db
from .conf import (
    override_get_db,
    client,
    test_event,
    test_bet,
    test_user,
)
from constants import Status

app.dependency_overrides[get_db] = override_get_db


def test_create_event():
    response = client.post("/events/")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == Status.NOT_PLAYED


def test_update_event(test_event, test_bet):
    response = client.put(f"/events/{test_event.id}", json={"status": Status.WIN.name})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == Status.WIN.value
    assert test_bet.status == Status.WIN.value

    response = client.put(f"/events/{test_event.id}", json={"status": Status.LOSE.name})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
