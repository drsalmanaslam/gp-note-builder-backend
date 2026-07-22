from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

db = SessionLocal()
admin = db.query(User).filter(User.username == "admin").first()
if admin:
    admin.hashed_password = get_password_hash("Admin123!")
    admin.role = "admin"
    db.commit()
    print("Admin password reset! Username: admin, Password: Admin123!")
else:
    print("No admin found.")
db.close()