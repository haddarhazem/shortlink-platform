from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration, read from SHORTLINK_* environment variables."""

    model_config = SettingsConfigDict(env_prefix="SHORTLINK_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://shortlink:shortlink@localhost:5432/shortlink"
    base_url: str = "http://localhost:8000"
    code_length: int = 7


@lru_cache
def get_settings() -> Settings:
    return Settings()
