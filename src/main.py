from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from src.config import get_settings
from src.database.core import sessionmanager
from src.games.views import router as games_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    sessionmanager.init(settings.database_url)

    yield

    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(title="Collections API", lifespan=lifespan)

router = APIRouter(prefix="/api/v1")
router.include_router(games_router, prefix="/games", tags=["games"])

app.include_router(router)
