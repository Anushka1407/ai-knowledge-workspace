import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from app.api.documents import router as documents_router

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log when the app starts and shuts down."""
    logger.info("AI Knowledge Workspace API is starting up")
    yield
    logger.info("AI Knowledge Workspace API is shutting down")


app = FastAPI(
    title="AI Knowledge Workspace API",
    description="Backend API for the AI Knowledge Workspace.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(documents_router)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Return the health status of the API."""
    logger.info("Health check called")
    return {"status": "ok"}