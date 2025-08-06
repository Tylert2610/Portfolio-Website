from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ....database import get_db
from ....models import Category
from ....schemas import Category as CategorySchema

router = APIRouter()


@router.get("/", response_model=List[CategorySchema])
async def get_categories(db: Session = Depends(get_db)):
    """Get all categories"""
    categories = db.query(Category).order_by(Category.name).all()
    return categories 