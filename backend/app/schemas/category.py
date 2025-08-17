from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    slug: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class Category(CategoryBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
