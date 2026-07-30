"""
Script to create GP-Related Topics category and move non-clinical templates
Run: python move_to_gp_related.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Template, Category
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the templates to move (PSA Shared Decision-Making stays in Men's Health)
TEMPLATES_TO_MOVE = [
    "Medication Review",
    "NDLS Medical Form - Group 1",
    "NDLS Medical Form - Group 2",
    "Conditional Logic Demo"
]

NEW_CATEGORY_NAME = "GP-Related Topics"

def create_gp_related_category(db):
    """Create the GP-Related Topics category if it doesn't exist"""
    category = db.query(Category).filter(Category.name == NEW_CATEGORY_NAME).first()
    if not category:
        logger.info(f"Creating new category: {NEW_CATEGORY_NAME}")
        category = Category(name=NEW_CATEGORY_NAME)
        db.add(category)
        db.commit()
        db.refresh(category)
        logger.info(f"✅ Category '{NEW_CATEGORY_NAME}' created with ID: {category.id}")
    else:
        logger.info(f"✅ Category '{NEW_CATEGORY_NAME}' already exists (ID: {category.id})")
    return category

def move_templates_to_gp_related(db, category):
    """Move specified templates to GP-Related Topics category"""
    updated_count = 0
    not_found = []
    
    for template_title in TEMPLATES_TO_MOVE:
        # Find template by title (case-insensitive)
        templates = db.query(Template).filter(
            Template.title.ilike(f"%{template_title}%")
        ).all()
        
        if not templates:
            logger.warning(f"⚠️ Template not found: '{template_title}'")
            not_found.append(template_title)
            continue
        
        for template in templates:
            old_category = template.category
            template.category = NEW_CATEGORY_NAME
            template.updated_at = datetime.now(timezone.utc)
            db.commit()
            updated_count += 1
            logger.info(f"✅ Moved: '{template.title}' from '{old_category}' → '{NEW_CATEGORY_NAME}'")
    
    return updated_count, not_found

def main():
    """Main execution"""
    logger.info("=" * 60)
    logger.info("GP-Related Topics Category Migration")
    logger.info("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Step 1: Create the category
        category = create_gp_related_category(db)
        
        # Step 2: Move templates
        logger.info("\n📁 Moving templates to GP-Related Topics...")
        updated_count, not_found = move_templates_to_gp_related(db, category)
        
        # Step 3: Summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 Migration Summary")
        logger.info("=" * 60)
        logger.info(f"✅ Templates moved: {updated_count}")
        
        if not_found:
            logger.warning(f"⚠️ Templates not found: {not_found}")
        
        # Step 4: Verify the new category has templates
        gp_templates = db.query(Template).filter(
            Template.category == NEW_CATEGORY_NAME
        ).all()
        
        logger.info(f"\n📁 Templates now in '{NEW_CATEGORY_NAME}':")
        for t in gp_templates:
            logger.info(f"   - {t.title}")
        
        logger.info("\n✅ Migration completed successfully!")
        
        # Step 5: Verify PSA is still in Men's Health
        psa_templates = db.query(Template).filter(
            Template.title.ilike("%PSA%")
        ).all()
        
        if psa_templates:
            logger.info(f"\n🔍 PSA templates still in their categories:")
            for t in psa_templates:
                logger.info(f"   - {t.title} → {t.category} (unchanged)")
        
    except Exception as e:
        logger.error(f"❌ Error during migration: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()