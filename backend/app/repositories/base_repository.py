# backend/app/repositories/base_repository.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class IRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    """
    Abstract base class for data repositories.
    Defines the standard CRUD interface.
    """

    @abstractmethod
    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        pass

    @abstractmethod
    async def get(self, id: Any) -> Optional[ModelType]:
        """Get a single record by its ID."""
        pass

    @abstractmethod
    async def list(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get a list of records with pagination."""
        pass

    @abstractmethod
    async def update(self, *, id: Any, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        """Update a record by its ID."""
        pass

    @abstractmethod
    async def delete(self, *, id: Any) -> Optional[ModelType]:
        """Delete a record by its ID."""
        pass