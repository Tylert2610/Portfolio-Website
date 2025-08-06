from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ....database import get_db
from ....models import Post as PostModel, Category as CategoryModel, Subscriber as SubscriberModel, User as UserModel
from ....schemas import PostCreate, PostUpdate, CategoryCreate, CategoryUpdate, User, UserCreate, UserLogin, Token, Post, Category, Subscriber
from ....core.security import verify_password, get_password_hash, create_access_token, verify_token
from ....core.email import email_service
from slugify import slugify

router = APIRouter()
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserModel:
    """Get current authenticated user"""
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Admin login"""
    user = db.query(UserModel).filter(UserModel.username == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Post management endpoints
@router.post("/posts", response_model=Post)
async def create_post(
    post: PostCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new blog post"""
    # Generate slug if not provided
    if not post.slug:
        post.slug = slugify(post.title)
    
    # Check if slug already exists
    existing_post = db.query(PostModel).filter(PostModel.slug == post.slug).first()
    if existing_post:
        raise HTTPException(status_code=400, detail="Post with this slug already exists")
    
    db_post = PostModel(
        title=post.title,
        slug=post.slug,
        content=post.content,
        excerpt=post.excerpt,
        read_time=post.read_time,
        category_id=post.category_id,
        author_id=current_user.id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post


@router.put("/posts/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a blog post"""
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Update fields
    for field, value in post_update.dict(exclude_unset=True).items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    
    return db_post


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a blog post"""
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    
    return {"message": "Post deleted successfully"}


@router.post("/posts/{post_id}/publish")
async def publish_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Publish a blog post and notify subscribers"""
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.published_at:
        raise HTTPException(status_code=400, detail="Post is already published")
    
    # Publish the post
    db_post.published_at = datetime.utcnow()
    db.commit()
    
    # Notify subscribers
    active_subscribers = db.query(SubscriberModel).filter(SubscriberModel.status == "active").all()
    subscriber_emails = [sub.email for sub in active_subscribers]
    
    if subscriber_emails:
        post_url = f"https://webbpulse.com/blog/{db_post.slug}"
        email_service.send_new_post_notification(subscriber_emails, db_post.title, post_url)
    
    return {"message": "Post published successfully"}


# Category management endpoints
@router.post("/categories", response_model=Category)
async def create_category(
    category: CategoryCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new category"""
    # Generate slug if not provided
    if not category.slug:
        category.slug = slugify(category.name)
    
    # Check if slug already exists
    existing_category = db.query(CategoryModel).filter(CategoryModel.slug == category.slug).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")
    
    db_category = CategoryModel(name=category.name, slug=category.slug)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.put("/categories/{category_id}", response_model=Category)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a category"""
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Update fields
    for field, value in category_update.dict(exclude_unset=True).items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    
    return db_category


# Subscriber management endpoints
@router.get("/subscribers", response_model=List[Subscriber])
async def get_subscribers(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all subscribers"""
    subscribers = db.query(SubscriberModel).order_by(SubscriberModel.subscribed_at.desc()).all()
    return subscribers 