from app.database import SessionLocal
from app.models import User

db = SessionLocal()
old = db.query(User).filter(User.username == "admin").first()
if old:
    db.delete(old)
    db.commit()
    print("Deleted old admin!")
else:
    print("Old admin not found")
db.close()