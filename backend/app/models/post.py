from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(Text, nullable=True)
    read_time = Column(String, nullable=True)  # e.g., "5 min read"
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    category_id = Column(
        Integer, ForeignKey("categories.id"), nullable=True
    )  # Blog post category
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    category = relationship("Category", back_populates="posts")  # Blog post category
    author = relationship("User", back_populates="posts")
