# backend/app/repositories/impl/user_repository_mongo.py
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.user import UserCreate, UserUpdate, UserMongo

from app.repositories.base_repository import IRepository

class UserRepositoryMongo(IRepository[UserMongo, UserCreate, UserUpdate]):
    """
    MongoDB repository implementation for User data.
    """
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def get(self, id: str) -> Optional[UserMongo]:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        return UserMongo(**doc) if doc else None

    async def get_by_email(self, *, email: str) -> Optional[UserMongo]:
        doc = await self.collection.find_one({"email": email})
        return UserMongo(**doc) if doc else None

    async def list(self, *, skip: int = 0, limit: int = 100) -> List[UserMongo]:
        cursor = self.collection.find().skip(skip).limit(limit)
        users = await cursor.to_list(length=limit)
        return [UserMongo(**user) for user in users]

    async def create(self, *, obj_in: UserCreate, hashed_password: str) -> UserMongo:
        user_data = obj_in.model_dump()
        user_data["hashed_password"] = hashed_password
        
        result = await self.collection.insert_one(user_data)
        created_user = await self.get(str(result.inserted_id))
        return created_user

    async def update(self, *, id: str, obj_in: UserUpdate, hashed_password: Optional[str] = None) -> Optional[UserMongo]:
        update_data = obj_in.model_dump(exclude_unset=True)
        if hashed_password:
            update_data["hashed_password"] = hashed_password
            
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if result.modified_count == 1:
            return await self.get(id)
        return None

    async def delete(self, *, id: str) -> Optional[UserMongo]:
        user_to_delete = await self.get(id)
        if user_to_delete:
            await self.collection.delete_one({"_id": ObjectId(id)})
        return user_to_delete