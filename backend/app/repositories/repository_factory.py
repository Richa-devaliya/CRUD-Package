# backend/app/repositories/repository_factory.py
from app.core.config import settings
from app.repositories.base_repository import IRepository
from app.repositories.impl.user_repository_postgres import UserRepositoryPostgres
from app.repositories.impl.user_repository_mongo import UserRepositoryMongo

class RepositoryFactory:
    """
    Factory class to get repository instances based on DB configuration.
    """
    @staticmethod
    def get_user_repository(db_session) -> IRepository:
        """
        Returns a user repository instance based on the configured database type.
        
        Args:
            db_session: The database session object.
        
        Returns:
            An instance of a class that implements IRepository.
        """
        if settings.DB_TYPE == "postgres":
            return UserRepositoryPostgres(db_session)
        elif settings.DB_TYPE == "mongo":
            return UserRepositoryMongo(db_session)
        else:
            raise ValueError(f"Unsupported DB_TYPE: {settings.DB_TYPE}")