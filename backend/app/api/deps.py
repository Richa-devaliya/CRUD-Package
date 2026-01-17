# backend/app/api/deps.py
from typing import Generator

from fastapi.params import Depends
from app.core.config import settings
from app.db.pg_session import pg_session
from app.db.mongo_session import mongo_session
from app.repositories.repository_factory import RepositoryFactory
from app.services.user_service import UserService

async def get_db_session():
    """
    Dependency to get a database session based on configuration.
    """
    if settings.DB_TYPE == "postgres":
        async for session in pg_session.get_db():
            yield session
    elif settings.DB_TYPE == "mongo":
        yield mongo_session.get_db()
    else:
        raise ValueError(f"Unsupported DB_TYPE: {settings.DB_TYPE}")


def get_user_service(db_session = Depends(get_db_session)) -> UserService:
    """
    Dependency to get the UserService instance with the appropriate repository.
    """
    user_repo = RepositoryFactory.get_user_repository(db_session)
    return UserService(user_repo)