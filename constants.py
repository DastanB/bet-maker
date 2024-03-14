from enum import Enum


class Status(str, Enum):
    WIN = "Выиграло"
    LOSE = "Проиграло"
    NOT_PLAYED = "Не сыграло"
