from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from ..database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String, nullable=True)  # URL to project image
    technologies = Column(JSON, nullable=False, default=list)
    github_url = Column(String, nullable=True)
    live_url = Column(String, nullable=True)
    featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)  # For soft deletes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
