"""
Gestiva Security (GestivaSec V1) — Core Configuration & Settings Loader
Centralized environment configuration for self-hosted, portable SOC deployments.
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # DATABASE & STORAGE
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/gestivasec")
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./storage")
    
    # REDIS
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # AUTH & SECURITY
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-in-production-2026")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-jwt-key-change-in-production-2026")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:8000,http://localhost:3000,http://127.0.0.1:8000")

settings = Settings()
