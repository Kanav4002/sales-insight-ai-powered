from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings, configure_logging
from .routes import upload


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Sales Insight Automator API",
        description="Backend service for generating AI-powered sales summaries.",
        version="0.1.0",
    )

    allowed_origins = settings.cors_origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(upload.router, prefix="/api", tags=["upload"])

    @app.get("/health", tags=["health"])
    async def health_check() -> dict:
        return {"status": "healthy"}

    return app


app = create_app()

