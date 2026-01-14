import os
import sys

import pytest
from httpx import ASGITransport, AsyncClient


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import get_settings
from src.main import app


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="function", autouse=True)
def async_client(settings) -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url=settings.get_api_url)
