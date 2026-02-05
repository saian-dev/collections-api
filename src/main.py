from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI

from src.config import get_settings
from src.database.core import sessionmanager
from src.games.views import router as games_router


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    sessionmanager.init(settings.database_url)

    yield

    if sessionmanager._engine is not None:
        await sessionmanager.close()


def setup_routes() -> APIRouter:
    router = APIRouter(prefix=settings.api_prefix)
    router.include_router(games_router, prefix="/games", tags=["games"])
    return router


app = FastAPI(title="Collections API", lifespan=lifespan)
app.include_router(setup_routes())


if __name__ == "__main__":
    uvicorn.run(app, host=settings.base_url.host, port=settings.base_url.port)  # type: ignore[arg-type]
