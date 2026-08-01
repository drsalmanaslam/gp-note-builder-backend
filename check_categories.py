from app.database import SessionLocal
from app.models import Category, Template
from sqlalchemy import func

db = SessionLocal()

# Get categories with template counts
categories = db.query(Category).all()
print("Categories with template counts:")
for cat in categories:
    count = db.query(Template).filter(Template.category == cat.name).count()
    print(f"  {cat.name}: {count} templates")

# Also check the template_count field if it exists
print("\nChecking if template_count field exists:")
try:
    for cat in categories:
        if hasattr(cat, 'template_count'):
            print(f"  {cat.name}: template_count={cat.template_count}")
        else:
            print("  No template_count field found on Category model")
            break
except Exception as e:
    print(f"Error: {e}")

db.close()