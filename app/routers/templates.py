import json
from reportlab.lib.pagesizes import letter
from datetime import datetime, timezone
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from fastapi.responses import StreamingResponse, JSONResponse
import io

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional
from datetime import datetime, timezone
from app.database import get_db
from app.models import User, Template, Category, UserActivity, user_favourites, TemplateVersion
from app.schemas import (
    TemplateCreate, TemplateUpdate, TemplateResponse,
    TemplateVersionResponse, CategoryResponse, FavouriteResponse,
    ActivityResponse
)
from app.auth import get_current_active_user

router = APIRouter(prefix="/templates", tags=["templates"])

# ============ TEMPLATE CRUD ============

@router.get("/", response_model=List[TemplateResponse])
def get_templates(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Template).filter(Template.deleted_at.is_(None))  # ← ADD THIS LINE
    
    # ... rest of the code
    if category:
        query = query.filter(Template.category == category)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Template.title.ilike(search_term),
                Template.description.ilike(search_term)
            )
        )
    
    query = query.filter(
        or_(
            Template.is_public == True,
            Template.created_by == current_user.id
        )
    )
    
    query = query.order_by(Template.created_at.desc())
    templates = query.offset(skip).limit(limit).all()
    
    favourite_ids = set()
    for fav in current_user.favourite_templates:
        favourite_ids.add(fav.id)
    
    result = []
    for template in templates:
        template_dict = TemplateResponse.model_validate(template)
        template_dict.is_favourite = template.id in favourite_ids
        result.append(template_dict)
    
    return result

@router.get("/{template_id}", response_model=TemplateResponse)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific template by ID"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if not template.is_public and template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    template.view_count += 1
    db.commit()
    
    activity = UserActivity(
        user_id=current_user.id,
        template_id=template.id,
        action="view"
    )
    db.add(activity)
    db.commit()
    
    is_favourite = any(fav.id == template.id for fav in current_user.favourite_templates)
    
    response = TemplateResponse.model_validate(template)
    response.is_favourite = is_favourite
    
    return response

@router.post("/", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
def create_template(
    template: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Get or create category
    category = db.query(Category).filter(Category.name == template.category).first()
    if not category:
        category = Category(name=template.category)
        db.add(category)
        db.commit()
        db.refresh(category)
    
    db_template = Template(
        title=template.title,
        description=template.description,
        category=template.category,
        category_id=category.id,  # NEW: Set category_id
        content=template.content,
        is_public=template.is_public,
        created_by=current_user.id
    )
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    return db_template

# ============ UPDATE TEMPLATE (ONLY ONE!) ============

@router.put("/{template_id}", response_model=TemplateResponse)
def update_template(
    template_id: int,
    template_update: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a template"""
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if db_template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Save version history
    if template_update.content is not None and template_update.content != db_template.content:
        version = TemplateVersion(
            template_id=db_template.id,
            version=db_template.version + 1,
            content=db_template.content,
            changes="Updated content"
        )
        db.add(version)
        db_template.version += 1
    
    # Update fields
    if template_update.title is not None:
        db_template.title = template_update.title
    if template_update.description is not None:
        db_template.description = template_update.description
    if template_update.category is not None:
        db_template.category = template_update.category
    if template_update.content is not None:
        db_template.content = template_update.content
    if template_update.is_public is not None:
        db_template.is_public = template_update.is_public
    
    db.commit()
    db.refresh(db_template)
    
    return db_template

@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if db_template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Soft delete - mark as deleted instead of removing from database
    db_template.deleted_at = datetime.now(timezone.utc)
    db.commit()

# ============ CATEGORIES ============

@router.get("/categories/all", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all categories with template counts"""
    categories = db.query(Category).all()
    result = []
    for category in categories:
        count = db.query(Template).filter(
            Template.category == category.name,
            or_(
                Template.is_public == True,
                Template.created_by == current_user.id
            )
        ).count()
        
        category_dict = CategoryResponse.model_validate(category)
        category_dict.template_count = count
        result.append(category_dict)
    
    return result

# ============ FAVOURITES ============

@router.post("/{template_id}/favourite", response_model=FavouriteResponse)
def add_favourite(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add a template to favourites"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template in current_user.favourite_templates:
        raise HTTPException(status_code=400, detail="Already in favourites")
    
    current_user.favourite_templates.append(template)
    db.commit()
    
    activity = UserActivity(
        user_id=current_user.id,
        template_id=template.id,
        action="favourite"
    )
    db.add(activity)
    db.commit()
    
    return FavouriteResponse(template_id=template_id, created_at=datetime.now(timezone.utc))

@router.delete("/{template_id}/favourite", status_code=status.HTTP_204_NO_CONTENT)
def remove_favourite(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove a template from favourites"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template not in current_user.favourite_templates:
        raise HTTPException(status_code=400, detail="Not in favourites")
    
    current_user.favourite_templates.remove(template)
    db.commit()

@router.get("/favourites/list", response_model=List[TemplateResponse])
def get_favourites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all favourited templates"""
    templates = current_user.favourite_templates
    result = []
    for template in templates:
        template_dict = TemplateResponse.model_validate(template)
        template_dict.is_favourite = True
        result.append(template_dict)
    
    return result

# ============ RECENT ACTIVITY ============

@router.get("/recent/used", response_model=List[TemplateResponse])
def get_recent_templates(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get recently used templates"""
    activities = db.query(UserActivity).filter(
        UserActivity.user_id == current_user.id,
        UserActivity.action == "view"
    ).order_by(UserActivity.created_at.desc()).limit(limit).all()
    
    template_ids = [activity.template_id for activity in activities]
    templates = db.query(Template).filter(Template.id.in_(template_ids)).all()
    
    template_map = {t.id: t for t in templates}
    result = []
    seen_ids = set()
    for activity in activities:
        if activity.template_id in template_map and activity.template_id not in seen_ids:
            seen_ids.add(activity.template_id)
            template = template_map[activity.template_id]
            template_dict = TemplateResponse.model_validate(template)
            template_dict.is_favourite = template in current_user.favourite_templates
            result.append(template_dict)

    return result

# ============ TEMPLATE VERSIONS ============

@router.get("/{template_id}/versions", response_model=List[TemplateVersionResponse])
def get_template_versions(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get version history of a template"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    versions = db.query(TemplateVersion).filter(
        TemplateVersion.template_id == template_id
    ).order_by(TemplateVersion.version.desc()).all()
    
    return versions
# ============ SHARE FUNCTIONALITY ============

@router.post("/{template_id}/share")
def create_share_link(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a shareable link for a template."""
    import secrets
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    share_token = secrets.token_urlsafe(32)
    
    template.share_token = share_token
    template.share_created_at = datetime.now(timezone.utc)
    template.share_views = 0
    
    db.commit()
    db.refresh(template)
    
    return {
        "share_token": share_token,
        "share_url": f"/share/{share_token}",
        "share_created_at": template.share_created_at,
        "share_views": 0
    }

@router.get("/share/{share_token}")
def get_shared_template(
    share_token: str,
    db: Session = Depends(get_db)
):
    """View a template via share link (no authentication required)."""
    template = db.query(Template).filter(Template.share_token == share_token).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template.share_views += 1
    db.commit()
    
    return {
        "id": template.id,
        "title": template.title,
        "description": template.description,
        "category": template.category,
        "content": template.content,
        "creator_username": template.creator.username if template.creator else None,
        "share_views": template.share_views,
        "created_at": template.created_at,
        "is_public": template.is_public
    }

@router.get("/{template_id}/share-info")
def get_share_info(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get share information for a template."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "share_token": template.share_token,
        "share_views": template.share_views or 0,
        "share_created_at": template.share_created_at,
        "share_url": f"/share/{template.share_token}" if template.share_token else None,
        "is_public": template.is_public
    }

@router.delete("/{template_id}/share")
def remove_share_link(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove the share link for a template."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    template.share_token = None
    template.share_created_at = None
    template.share_views = 0
    
    db.commit()
    
    return {"message": "Share link removed successfully"}

@router.post("/{template_id}/copy", response_model=TemplateResponse)
def copy_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a copy of an existing template."""
    original = db.query(Template).filter(Template.id == template_id).first()
    if not original:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check if user has access to the original
    if not original.is_public and original.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Create copy
    new_template = Template(
        title=f"{original.title} (Copy)",
        description=original.description,
        category=original.category,
        content=original.content,
        is_public=original.is_public,
        created_by=current_user.id
    )
    
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    
    return new_template

# ============ EXPORT TEMPLATES ============

@router.get("/{template_id}/export/json")
def export_template_json(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Export template as JSON."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check access
    if not template.is_public and template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Prepare export data
    export_data = {
        "id": template.id,
        "title": template.title,
        "description": template.description,
        "category": template.category,
        "content": template.content,
        "version": template.version,
        "created_at": template.created_at.isoformat() if template.created_at else None,
        "updated_at": template.updated_at.isoformat() if template.updated_at else None,
        "created_by": template.creator.username if template.creator else None,
        "is_public": template.is_public
    }
    
    # Return as JSON download
    json_str = json.dumps(export_data, indent=2, default=str)
    
    return StreamingResponse(
        io.BytesIO(json_str.encode()),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={template.title.replace(' ', '_')}.json"}
    )

@router.get("/{template_id}/export/pdf")
def export_template_pdf(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Export template as PDF."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check access
    if not template.is_public and template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    body_style = styles['BodyText']
    
    # Custom styles
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading3'],
        fontSize=14,
        textColor='#2563eb',
        spaceAfter=12
    )
    
    content = []
    
    # Title
    content.append(Paragraph(f"<b>{template.title}</b>", title_style))
    content.append(Spacer(1, 0.25 * inch))
    
    # Metadata
    content.append(Paragraph(f"<b>Category:</b> {template.category}", body_style))
    content.append(Paragraph(f"<b>Version:</b> {template.version}", body_style))
    content.append(Paragraph(f"<b>Created:</b> {template.created_at.strftime('%B %d, %Y') if template.created_at else 'N/A'}", body_style))
    if template.creator:
        content.append(Paragraph(f"<b>Created by:</b> {template.creator.username}", body_style))
    content.append(Spacer(1, 0.25 * inch))
    
    # Description
    if template.description:
        content.append(Paragraph(f"<b>Description:</b>", heading_style))
        content.append(Paragraph(template.description, body_style))
        content.append(Spacer(1, 0.25 * inch))
    
    # Content Sections
    content.append(Paragraph("<b>Content</b>", heading_style))
    content.append(Spacer(1, 0.1 * inch))
    
    if template.content and template.content.get('sections'):
        for section in template.content['sections']:
            title = section.get('title', 'Untitled Section')
            body = section.get('body', 'No content')
            content.append(Paragraph(f"<b>{title}</b>", section_style))
            content.append(Paragraph(body, body_style))
            content.append(Spacer(1, 0.15 * inch))
    
    doc.build(content)
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={template.title.replace(' ', '_')}.pdf"}
    )

# ============ IMPORT TEMPLATE ============

@router.post("/import", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
def import_template(
    template_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Import a template from JSON data"""
    # Get or create category
    category_name = template_data.get("category", "Imported")
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    db_template = Template(
        title=template_data.get("title", "Imported Template"),
        description=template_data.get("description", ""),
        category=category_name,
        category_id=category.id,
        content=template_data.get("content", {"sections": []}),
        is_public=template_data.get("is_public", False),
        created_by=current_user.id
    )

    db.add(db_template)
    db.commit()
    db.refresh(db_template)

    return db_template