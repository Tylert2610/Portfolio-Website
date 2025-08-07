from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .category import Category


class PostBase(BaseModel):
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    read_time: Optional[str] = None
    category_id: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    read_time: Optional[str] = None
    category_id: Optional[int] = None
    published_at: Optional[datetime] = None


class Post(PostBase):
    id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[Category] = None

    class Config:
        from_attributes = True


class PostList(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    read_time: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime
    category: Optional[Category] = None

    class Config:
        from_attributes = True 