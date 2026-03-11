import logging
from functools import lru_cache
from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    environment: str = "development"
    debug: bool = True
    frontend_url: AnyHttpUrl | None = None
    groq_api_key: str | None = None
    groq_model: str = "llama-3.1-70b-versatile"
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from_email: str | None = None
    rate_limit_requests_per_minute: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def cors_origins(self) -> List[str]:
        origins: List[str] = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
        if self.frontend_url:
            origins.append(str(self.frontend_url))
        return origins


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def configure_logging() -> None:
    log_level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

