from functools import lru_cache
from urllib.parse import urljoin

from dotenv import find_dotenv
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    test_database_url: str | None = None
    base_url: HttpUrl = HttpUrl("http://0.0.0.0:8000")
    api_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=find_dotenv(".env", usecwd=True), extra="ignore")

    @property
    def get_api_url(self) -> str:
        return urljoin(str(self.base_url), self.api_prefix)


@lru_cache
def get_settings() -> Settings:
    return Settings()
