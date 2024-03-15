import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    # App
    APP_NAME:  str = os.environ.get("APP_NAME", "FastAPI")
    DEBUG: bool = bool(os.environ.get("DEBUG", False))

    # Postgresql Database Config
    POSTGRESQL_HOST: str = os.environ.get("POSTGRESQL_HOST", 'localhost')
    POSTGRESQL_USER: str = os.environ.get("POSTGRESQL_USER", 'root')
    POSTGRESQL_PASS: str = os.environ.get("POSTGRESQL_PASSWORD", 'secret')
    POSTGRESQL_PORT: int = int(os.environ.get("POSTGRESQL_PORT", 5432))
    POSTGRESQL_DB: str = os.environ.get("POSTGRESQL_DB", 'fastapi')
    DATABASE_URI: str = f"postgresql+asyncpg://{POSTGRESQL_USER}:%s@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DB}" % quote_plus(POSTGRESQL_PASS)

    # App Secret Key
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
