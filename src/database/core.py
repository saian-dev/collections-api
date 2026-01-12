import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, connection_str: str) -> None:
        self._engine = create_async_engine(connection_str)
        self._sessionmaker = async_sessionmaker(self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("Database session manager has not been initialized.")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("Database session manager is not initialized")

        async with self._sessionmaker() as session:
            async with session.begin():
                yield session

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("Database session manager is not initialized")

        async with self._engine.begin() as connection:
            yield connection


sessionmanager = DatabaseSessionManager()


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
