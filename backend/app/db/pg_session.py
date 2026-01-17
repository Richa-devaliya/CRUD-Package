# backend/app/db/pg_session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

class PostgresSessionManager:
    """
    Manages the connection and session to the PostgreSQL database.
    """
    def __init__(self):
        self._engine = None
        self._session_factory = None

    def init_db(self):
        """
        Initializes the database engine and session factory.
        """
        if settings.DB_TYPE == "postgres":
            self._engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
            self._session_factory = sessionmaker(
                autocommit=False, autoflush=False, bind=self._engine, class_=AsyncSession
            )

    async def close_db(self):
        """
        Closes the database engine connections.
        """
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
    
    async def get_db(self) -> AsyncSession:
        """
        Provides a database session for a single request.
        """
        if self._session_factory is None:
            raise Exception("Database not initialized. Call init_db() first.")
        async with self._session_factory() as session:
            yield session

pg_session = PostgresSessionManager()