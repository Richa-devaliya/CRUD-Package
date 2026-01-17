# backend/app/decorators/transaction.py
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings

def transactional(func):
    """
    Decorator to wrap a function in a database transaction for PostgreSQL.
    """
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        # Only apply transaction for postgres
        if settings.DB_TYPE != "postgres":
            return await func(self, *args, **kwargs)

        # Assumes the repository is available as self.repo.db
        db: AsyncSession = self.user_repo.db
        
        async with db.begin():
            try:
                result = await func(self, *args, **kwargs)
                await db.commit()
                return result
            except Exception as e:
                await db.rollback()
                raise e
    return wrapper