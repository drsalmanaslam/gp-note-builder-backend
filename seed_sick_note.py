from app.database import SessionLocal
from app.models import User, Template

def seed_sick_note():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Sick Note / Fit Note (MED3)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_sick_note()