from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import User, Category, Template
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from app.auth import get_current_active_user

router = APIRouter(prefix="/categories", tags=["categories"])

# Get all categories (public)
@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    categories = db.query(Category).filter(
        Category.is_active == True
    ).offset(skip).limit(limit).all()
    
    result = []
    for category in categories:
        count = db.query(Template).filter(
            Template.category == category.name,
            Template.is_public == True
        ).count()
        category_dict = CategoryResponse.model_validate(category)
        category_dict.template_count = count
        result.append(category_dict)
    
    return result

# Get single category
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_active == True
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    count = db.query(Template).filter(
        Template.category == category.name,
        Template.is_public == True
    ).count()
    category_dict = CategoryResponse.model_validate(category)
    category_dict.template_count = count
    return category_dict

# Create category (admin only)
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin access required."
        )
    
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    db_category = Category(
        name=category.name,
        icon=category.icon,
        description=category.description,
        color=category.color
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

# Update category (admin only)
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin access required."
        )
    
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category_update.name is not None:
        db_category.name = category_update.name
    if category_update.icon is not None:
        db_category.icon = category_update.icon
    if category_update.description is not None:
        db_category.description = category_update.description
    if category_update.color is not None:
        db_category.color = category_update.color
    if category_update.is_active is not None:
        db_category.is_active = category_update.is_active
    
    db.commit()
    db.refresh(db_category)
    
    return db_category

# Delete category (admin only - soft delete)
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin access required."
        )
    
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_category.is_active = False
    db.commit()