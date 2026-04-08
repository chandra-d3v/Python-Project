from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.addresses import router as address_router
from app.core.config import get_settings
from app.core.logging import configure_logging, logger
from app.db.base import Base
from app.db.session import engine
from app import models  # noqa: F401

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting %s", settings.app_name)
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables are ready")
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(address_router, prefix=settings.api_prefix)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}
