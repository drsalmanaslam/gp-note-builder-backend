"""
Clean up duplicate templates on Render (PostgreSQL)
Keeps the template with the highest view_count or most recent updated_at
"""
from app.database import SessionLocal
from app.models import Template
from sqlalchemy import func

db = SessionLocal()

# Find duplicate titles
duplicates = db.query(
    Template.title, 
    func.count(Template.id).label('count')
).group_by(Template.title).having(func.count(Template.id) > 1).all()

print(f"Found {len(duplicates)} duplicate title groups:")
for title, count in duplicates:
    print(f"  '{title}': {count} copies")

# For each duplicate, keep the best one and delete others
total_deleted = 0
for title, count in duplicates:
    copies = db.query(Template).filter(Template.title == title).order_by(
        Template.view_count.desc(), 
        Template.updated_at.desc()
    ).all()
    
    # Keep the first one (highest view_count, most recent)
    keep = copies[0]
    delete_list = copies[1:]
    
    for template in delete_list:
        print(f"  Deleting: ID={template.id}, view_count={template.view_count}, created={template.created_at}")
        db.delete(template)
        total_deleted += 1
    
    print(f"  Keeping: ID={keep.id}, view_count={keep.view_count}")

db.commit()
print(f"\n✅ Deleted {total_deleted} duplicate templates")
db.close()