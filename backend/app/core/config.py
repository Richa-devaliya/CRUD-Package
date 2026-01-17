# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    PROJECT_NAME: str = "CRUD Automation Project"
    API_V1_STR: str = "/api/v1"
    
    # Database configuration
    # Set DB_TYPE to 'postgres' or 'mongo'
    DB_TYPE: str = "postgres"

    # Postgres Settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # MongoDB Settings
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "crud_db"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()