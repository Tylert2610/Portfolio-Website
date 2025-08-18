from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ....core.security import get_current_user
from ....database import get_db
from ....models import Experience, User
from ....schemas import Experience as ExperienceSchema
from ....schemas import ExperienceCreate, ExperienceList, ExperienceUpdate

router = APIRouter()


@router.get("/", response_model=List[ExperienceList])
async def get_experience(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get all active experience entries with pagination"""
    experience_entries = (
        db.query(Experience)
        .filter(Experience.is_active)
        .order_by(Experience.start_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return experience_entries


@router.get("/{experience_id}", response_model=ExperienceSchema)
async def get_experience_entry(experience_id: int, db: Session = Depends(get_db)):
    """Get a single experience entry by ID"""
    experience = (
        db.query(Experience)
        .filter(Experience.id == experience_id, Experience.is_active)
        .first()
    )
    if not experience:
        raise HTTPException(status_code=404, detail="Experience entry not found")
    return experience


@router.post("/", response_model=ExperienceSchema)
async def create_experience(
    experience: ExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new experience entry (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to create experience entries"
        )

    db_experience = Experience(**experience.model_dump())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


@router.put("/{experience_id}", response_model=ExperienceSchema)
async def update_experience(
    experience_id: int,
    experience_update: ExperienceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an experience entry (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to update experience entries"
        )

    db_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience entry not found")

    update_data = experience_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_experience, field, value)

    db.commit()
    db.refresh(db_experience)
    return db_experience


@router.delete("/{experience_id}")
async def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete an experience entry (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete experience entries"
        )

    db_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience entry not found")

    db_experience.is_active = False
    db.commit()

    return {"message": "Experience entry deleted successfully"}
