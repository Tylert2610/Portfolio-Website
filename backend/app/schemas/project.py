from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional, List
from datetime import datetime


class ProjectBase(BaseModel):
    title: str
    description: str
    image: Optional[str] = None
    technologies: List[str] = []
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    featured: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    technologies: Optional[List[str]] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    featured: Optional[bool] = None
    is_active: Optional[bool] = None


class Project(ProjectBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProjectList(BaseModel):
    id: int
    title: str
    description: str
    image: Optional[str] = None
    technologies: List[str] = []
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    featured: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
