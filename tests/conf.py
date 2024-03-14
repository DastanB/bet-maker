import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app
from models import Base, Bets, Events, Users
from routers.auth import bcrypt_context
from constants import Status

SQL_ALCHEMY_DATABASE = "sqlite:///./testdb.db"

engine = create_engine(
    SQL_ALCHEMY_DATABASE,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "test_dastan", "id": 1}


client = TestClient(app)


@pytest.fixture
def test_user():
    user = Users(
        username="test_dastan",
        first_name="Dastan",
        last_name="Baitursynov",
        hashed_password=bcrypt_context.hash("1234"),
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def test_event():
    event = Events(status=Status.NOT_PLAYED)

    db = TestingSessionLocal()
    db.add(event)
    db.commit()

    yield event

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM events;"))
        connection.commit()


@pytest.fixture
def test_bet(test_event, test_user):
    bet = Bets(
        amount=10000,
        event_id=test_event.id,
        user_id=test_user.id,
        status=Status.NOT_PLAYED,
    )

    db = TestingSessionLocal()
    db.add(bet)
    db.commit()

    yield bet

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM bets;"))
        connection.commit()
