from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Category(Base):
    """
    Blog post categories for organizing and filtering blog content.
    Categories are used to group related blog posts together.
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String, nullable=False
    )  # Display name (e.g., "Technology", "Career Tips")
    slug = Column(
        String, unique=True, index=True, nullable=False
    )  # URL-friendly identifier
    description = Column(String, nullable=True)  # Optional description
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to blog posts
    posts = relationship("Post", back_populates="category")
