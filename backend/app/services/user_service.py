# backend/app/services/user_service.py
from typing import List, Optional
from app.repositories.base_repository import IRepository
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException
from pydantic import EmailStr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hashes a plain text password."""
    return pwd_context.hash(password)

class UserService:
    """
    Service layer containing business logic for user operations.
    """
    def __init__(self, user_repo: IRepository):
        self.user_repo = user_repo

    async def get_user(self, user_id: int):
        """
        Retrieves a user by their ID.
        """
        user = await self.user_repo.get(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_users(self, skip: int = 0, limit: int = 100) -> List:
        """
        Retrieves a list of users.
        """
        return await self.user_repo.list(skip=skip, limit=limit)

    async def create_user(self, user_in: UserCreate):
        """
        Creates a new user, checking for email uniqueness.
        """
        user = await self.user_repo.get_by_email(email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
        hashed_password = get_password_hash(user_in.password)
        return await self.user_repo.create(obj_in=user_in, hashed_password=hashed_password)

    async def update_user(self, user_id: int, user_in: UserUpdate):
        """
        Updates an existing user.
        """
        hashed_password = None
        if user_in.password:
            hashed_password = get_password_hash(user_in.password)
        
        updated_user = await self.user_repo.update(id=user_id, obj_in=user_in, hashed_password=hashed_password)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user

    async def delete_user(self, user_id: int):
        """
        Deletes a user by their ID.
        """
        deleted_user = await self.user_repo.delete(id=user_id)
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        return deleted_user