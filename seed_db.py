from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def seed_admin():
    db = SessionLocal()
    
    # Check if admin exists
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created!")
    else:
        print("Admin user already exists.")
    
    db.close()

if __name__ == "__main__":
    seed_admin()