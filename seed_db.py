from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def seed_admin():
    # Check if main admin exists
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        # Don't create admin - it should already exist from main.py
        print("⚠️ Main admin not found - will be created by main.py")
        return
    print("✅ Main admin exists")
    
    db.close()

if __name__ == "__main__":
    seed_admin()