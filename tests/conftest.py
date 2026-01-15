import pytest
from httpx import ASGITransport, AsyncClient

from src.config import get_settings
from src.database.core import Base, get_db_session, sessionmanager
from src.main import app


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="function")
async def async_client(settings):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=settings.get_api_url) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def session_override(settings):
    if not settings.test_database_url:
        raise ValueError("Please, provide test database url.")
    sessionmanager.init(settings.test_database_url)

    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def get_db_session_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db_session] = get_db_session_override

    yield

    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await sessionmanager.close()
