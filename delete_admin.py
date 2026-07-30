from app.database import SessionLocal
from app.models import User

db = SessionLocal()
admin = db.query(User).filter(User.username == "admin").first()

if admin:
    db.delete(admin)
    db.commit()
    print('✅ Admin user deleted successfully!')
else:
    print('ℹ️ Admin user not found')

db.close()