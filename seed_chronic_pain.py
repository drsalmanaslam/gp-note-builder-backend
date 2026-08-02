from app.database import SessionLocal
from app.models import User, Template

def seed_chronic_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Chronic Pain & Opioid Review"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_chronic_pain()