from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tesla Diagnostics Platform"
    
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "tesla_diagnostics"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        # Using SQLite for local development as requested
        return "sqlite+aiosqlite:///./tesla.db"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
