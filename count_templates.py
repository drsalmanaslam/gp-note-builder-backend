from app.database import SessionLocal
from app.models import Template

db = SessionLocal()
count = db.query(Template).count()
print(f'Total templates in database: {count}')
db.close()