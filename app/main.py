import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.api.dependencies.auth import verify_api_key
from app.api.router import router
from app.core.logging import setup_logging

setup_logging(level=logging.DEBUG)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    yield
    logger.info("Application finished")


app = FastAPI(title="Payment Service", lifespan=lifespan)

app.include_router(
    router, prefix="/api/v1", tags=["v1"], dependencies=[Depends(verify_api_key)]
)
