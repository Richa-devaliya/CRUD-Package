# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Shared properties
class UserBase(BaseModel):
    """
    Base Pydantic model for user data.
    """
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    """
    Pydantic model for creating a new user.
    """
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    """
    Pydantic model for updating an existing user.
    """
    password: Optional[str] = Field(None, min_length=8)

class UserInDBBase(UserBase):
    """
    Base model for user data stored in the database.
    """
    id: int

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    """
    Pydantic model for returning user data.
    """
    pass

# Mongo specific User schema
class UserMongo(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str

    class Config:
        from_attributes = True
        populate_by_name = True