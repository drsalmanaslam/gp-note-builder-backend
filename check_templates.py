from app.database import SessionLocal
from app.models import Template

db = SessionLocal()
templates = db.query(Template).all()

print(f'Total templates in database: {len(templates)}')
print('\nAll templates:')
for t in templates:
    print(f'  - {t.title} (ID: {t.id})')

db.close()