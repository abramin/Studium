"""
Application configuration using pydantic-settings.
"""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database
    POSTGRES_USER: str = "studium"
    POSTGRES_PASSWORD: str = "studium_dev_password"
    POSTGRES_DB: str = "studium"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    @property
    def database_url(self) -> str:
        """Generate database URL."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def redis_url(self) -> str:
        """Generate Redis URL."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # Celery
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""

    @property
    def celery_broker(self) -> str:
        """Generate Celery broker URL."""
        return self.CELERY_BROKER_URL or self.redis_url

    @property
    def celery_backend(self) -> str:
        """Generate Celery result backend URL."""
        return self.CELERY_RESULT_BACKEND or self.redis_url

    # Local Storage
    LOCAL_STORAGE_PATH: str = "/app/storage"
    UPLOAD_DIR: str = "/app/storage/uploads"
    PROCESSED_DIR: str = "/app/storage/processed"

    # Ollama API (local LLM)
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"

    # Embedding Settings
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    EMBEDDING_DIMENSION: int = 768  # nomic-embed-text default


settings = Settings()
