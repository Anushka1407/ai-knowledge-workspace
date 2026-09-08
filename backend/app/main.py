import logging
from time import perf_counter

from dotenv import load_dotenv
from fastapi import FastAPI, Request

load_dotenv()

from app.api.documents import router as documents_router

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Knowledge Workspace API",
    description="Backend API for the AI Knowledge Workspace.",
    version="0.1.0",
)

app.include_router(documents_router)


@app.on_event("startup")
async def startup_event():
    """Log when the app starts up."""
    logger.info("AI Knowledge Workspace API is starting up")


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Return the health status of the API."""
    logger.info("Health check called")
    return {"status": "ok"}