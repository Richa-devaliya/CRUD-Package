# backend/app/repositories/impl/user_repository_postgres.py
from typing import Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base_repository import IRepository

class UserRepositoryPostgres(IRepository[User, UserCreate, UserUpdate]):
    """
    PostgreSQL repository implementation for User data.
    """
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get(self, id: Any) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.id == id))
        return result.scalars().first()

    async def get_by_email(self, *, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def list(self, *, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: UserCreate, hashed_password: str) -> User:
        db_obj = User(
            full_name=obj_in.full_name,
            email=obj_in.email,
            hashed_password=hashed_password,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, id: int, obj_in: UserUpdate, hashed_password: Optional[str] = None
    ) -> Optional[User]:
        db_obj = await self.get(id=id)
        if not db_obj:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        if hashed_password:
            update_data["hashed_password"] = hashed_password
            
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, *, id: int) -> Optional[User]:
        db_obj = await self.get(id=id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
        return db_obj