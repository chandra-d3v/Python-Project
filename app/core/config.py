from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Address Book API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    database_url: str = Field(
        default="sqlite:///./address_book.db",
        description="SQLAlchemy database connection string.",
    )
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
