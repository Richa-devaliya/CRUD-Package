# backend/app/api/routes/users.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.services.user_service import UserService
from app.api import deps

router = APIRouter()

@router.get("/users", response_model=List[schemas.user.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(deps.get_user_service),
) -> Any:
    """Retrieve a list of users with pagination."""
    users = await user_service.get_users(skip=skip, limit=limit)
    return users

@router.post("/users", response_model=schemas.user.User, status_code=201)
async def create_user(
    *,
    user_in: schemas.UserCreate,
    user_service: UserService = Depends(deps.get_user_service),
) -> Any:
    """Create a new user."""
    user = await user_service.create_user(user_in=user_in)
    return user

@router.get("/users/{user_id}", response_model=schemas.user.User)
async def read_user_by_id(
    user_id: str, # Use str to be compatible with both int (PG) and ObjectId (Mongo)
    user_service: UserService = Depends(deps.get_user_service),
) -> Any:
    """Get a specific user by their ID."""
    user = await user_service.get_user(user_id=user_id)
    return user

@router.put("/users/{user_id}", response_model=schemas.user.User)
async def update_user(
    *,
    user_id: str,
    user_in: schemas.UserUpdate,
    user_service: UserService = Depends(deps.get_user_service),
) -> Any:
    """Update an existing user."""
    user = await user_service.update_user(user_id=user_id, user_in=user_in)
    return user

@router.delete("/users/{user_id}", response_model=schemas.user.User)
async def delete_user(
    *,
    user_id: str,
    user_service: UserService = Depends(deps.get_user_service),
) -> Any:
    """Delete a user."""
    user = await user_service.delete_user(user_id=user_id)
    return user