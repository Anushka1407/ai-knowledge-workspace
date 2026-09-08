from fastapi import FastAPI

from app.api.documents import router as documents_router

app = FastAPI(
    title="AI Knowledge Workspace API",
    description="Backend API for the AI Knowledge Workspace.",
    version="0.1.0",
)

app.include_router(documents_router)


@app.on_event("startup")
async def startup_event():
    """Log when the app starts up."""
    print("✓ AI Knowledge Workspace API is starting up")


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Return the health status of the API."""
    print("✓ Health check called")
    return {"status": "ok"}