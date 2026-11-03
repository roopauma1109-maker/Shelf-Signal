
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "ShelfSignal"
    environment: str = "local"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    gemini_fallback_model: str = "gemini-2.5-flash"

    gemini_input_cost_per_million: float | None = None
    gemini_output_cost_per_million: float | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
