from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def seed_admin():
    # Check if main admin exists
    db = SessionLocal()  # ← ADD THIS LINE
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    
    if not admin:
        # Don't create admin - it should already exist from main.py
        print("⚠️ Main admin not found - will be created by main.py")
    else:
        print("✅ Main admin exists")
    
    db.close()  # ← This will now work

if __name__ == "__main__":
    seed_admin()