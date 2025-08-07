from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ....database import get_db
from ....models import Post, Category
from ....schemas import PostList, Post as PostSchema

router = APIRouter()


@router.get("/", response_model=List[PostList])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category_slug: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all published posts with pagination and optional category filter"""
    query = db.query(Post).filter(Post.published_at.isnot(None))
    
    if category_slug:
        query = query.join(Category).filter(Category.slug == category_slug)
    
    posts = query.order_by(Post.published_at.desc()).offset(skip).limit(limit).all()
    return posts


@router.get("/{slug}", response_model=PostSchema)
async def get_post(slug: str, db: Session = Depends(get_db)):
    """Get a single post by slug"""
    post = db.query(Post).filter(Post.slug == slug, Post.published_at.isnot(None)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/category/{category_slug}", response_model=List[PostList])
async def get_posts_by_category(
    category_slug: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get posts by category slug"""
    posts = (
        db.query(Post)
        .join(Category)
        .filter(Category.slug == category_slug, Post.published_at.isnot(None))
        .order_by(Post.published_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts 