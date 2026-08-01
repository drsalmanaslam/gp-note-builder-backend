from app.database import SessionLocal
from app.models import User

db = SessionLocal()
admin_user = db.query(User).filter(User.username == "admin").first()

if admin_user:
    db.delete(admin_user)
    db.commit()
    print("✅ Admin user deleted successfully!")
else:
    print("ℹ️ Admin user not found")

db.close()