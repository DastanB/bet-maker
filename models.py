from constants import Status
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL, Enum


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(Status), nullable=False, default=Status.NOT_PLAYED)


class Bets(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(DECIMAL(precision=10, scale=2), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.NOT_PLAYED)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
