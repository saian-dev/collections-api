import enum
from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.core import Base
from src.models import TimeStampMixin


class GameStatus(enum.Enum):
    RELEASED = "RELEASED"
    ALPHA = "ALPHA"
    BETA = "BETA"
    EARLY_ACCESS = "EARLY ACCESS"
    OFFLINE = "OFFLINE"
    CANCELLED = "CANCELLED"
    RUMORED = "RUMORED"
    DELISTED = "DELISTED"


class Game(TimeStampMixin, Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    game_status: Mapped[GameStatus]
    summary: Mapped[str] = mapped_column(unique=True, nullable=False)
    release_date: Mapped[date] = mapped_column(nullable=False)
