"""
Application Settings using pydantic-settings
"""
import secrets
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    app_name: str = "FDE Workbench API"
    app_env: str = "development"
    app_debug: bool = True
    app_port: int = 8080

    # Database
    database_url: str = "mysql://root:password@localhost:3306/fde_workbench?charset=utf8mb4"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Elasticsearch
    es_host: str = "http://localhost:9200"

    # Milvus
    milvus_host: str = "localhost"
    milvus_port: int = 19530

    # AI Orchestrator
    ai_orchestrator_url: str = "http://localhost:8090"
    ai_orchestrator_timeout: int = 120

    # Auth
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 10080  # 7 days = 7 * 24 * 60 = 10080 minutes

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # External Integrations
    aone_api_url: Optional[str] = None
    aone_api_token: Optional[str] = None
    crm_api_url: Optional[str] = None
    crm_api_token: Optional[str] = None
    oss_endpoint: Optional[str] = None
    oss_access_key: Optional[str] = None
    oss_secret_key: Optional[str] = None
    oss_bucket: Optional[str] = None

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    @field_validator("jwt_secret_key", mode="after")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        if not v or len(v) < 16:
            raise ValueError(
                "JWT_SECRET_KEY must be at least 16 characters. "
                "Set it via environment variable or .env file. "
                f"Example: JWT_SECRET_KEY={secrets.token_hex(32)}"
            )
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()