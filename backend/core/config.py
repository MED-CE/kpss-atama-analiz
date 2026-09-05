import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory where config.py lives (backend/core)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")

class Settings(BaseSettings):
    PROJECT_NAME: str = "KPSS Merkezi Atama Analiz Platformu API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # We use sqlite for local dev fallback, but postgres for production
    DATABASE_URL: str = "sqlite+aiosqlite:///./kpss.db"
    
    # Cloud configs
    APPWRITE_API_KEY: str | None = None
    AZURE_STORAGE_CONNECTION_STRING: str | None = None
    SENTRY_DSN: str | None = None

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8", extra="ignore")

settings = Settings()
