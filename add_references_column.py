from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE templates ADD COLUMN clinical_references TEXT"))
        conn.commit()
        print("✅ Added clinical_references column to templates table")
    except Exception as e:
        if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
            print("✅ Column already exists")
        else:
            print(f"❌ Error: {e}")