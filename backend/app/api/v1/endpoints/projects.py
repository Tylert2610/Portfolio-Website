from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ....database import get_db
from ....models import Project
from ....schemas import (
    ProjectList,
    Project as ProjectSchema,
    ProjectCreate,
    ProjectUpdate,
)
from ....core.security import get_current_user
from ....models import User

router = APIRouter()


@router.get("/", response_model=List[ProjectList])
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    featured_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    """Get all active projects with pagination and optional featured filter"""
    query = db.query(Project).filter(Project.is_active == True)

    if featured_only:
        query = query.filter(Project.featured == True)

    projects = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a single project by ID"""
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.is_active == True)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectSchema)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new project (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create projects")

    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.put("/{project_id}", response_model=ProjectSchema)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a project (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update projects")

    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete a project (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete projects")

    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_project.is_active = False
    db.commit()

    return {"message": "Project deleted successfully"}
