from fastapi import FastAPI

app = FastAPI(
    title="AI Knowledge Workspace API",
    description="Backend API for the AI Knowledge Workspace.",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Return the health status of the API."""
    return {"status": "ok"}