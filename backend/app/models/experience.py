from sqlalchemy import (JSON, Boolean, Column, Date, DateTime, Integer, String,
                        Text)
from sqlalchemy.sql import func

from ..database import Base


class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    period = Column(String, nullable=False)  # e.g., "Jul 2024 - Present"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Optional for current positions
    description = Column(Text, nullable=False)
    technologies = Column(JSON, nullable=False, default=list)
    achievements = Column(JSON, nullable=False, default=list)
    is_active = Column(Boolean, default=True)  # For soft deletes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
