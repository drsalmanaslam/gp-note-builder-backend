from fastapi import FastAPI, Depends
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import categories, notes
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import users, products, items, auth, templates, password_reset
from app.database import engine, Base
import os

# Create tables
Base.metadata.create_all(bind=engine)
# Ensure clinical_references column exists on Render PostgreSQL
from sqlalchemy import text
try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE templates ADD COLUMN IF NOT EXISTS clinical_references TEXT"))
        conn.commit()
        print("✅ clinical_references column ready")
except Exception as e:
    print(f"Column check (non-critical): {e}")

# Auto-seed templates on first startup (only if database is empty)
from app.database import SessionLocal
from app.models import Template, User
from app.auth import get_password_hash, get_current_admin
import importlib

db_check = SessionLocal()
existing_templates = db_check.query(Template).count()
db_check.close()

if existing_templates == 0:
    print("No templates found. Auto-seeding all templates...")
    seed_files = sorted([f.replace('.py', '') for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')])
    for seed_name in seed_files:
        try:
            mod = importlib.import_module(seed_name)
            for attr in dir(mod):
                if attr.startswith('seed_') and callable(getattr(mod, attr)):
                    getattr(mod, attr)()
                    break
            import time; time.sleep(0.5)  # Prevent connection pool exhaustion
        except Exception as e:
            print(f"❌ {seed_name}: {str(e)[:50]}")
    print("Auto-seeding complete!")
else:
    print(f"{existing_templates} templates already exist. Skipping seed.")

# Ensure admin has lifetime access
db = SessionLocal()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "gpclinicaldirector@notebuilder")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@gpnotebuilder.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "@GPLenovo!notes")

admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()
if not admin:
    admin = User(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        hashed_password=get_password_hash(ADMIN_PASSWORD),
        role="admin",
        is_active=True,
        subscription_status="active",
        subscription_plan="enterprise"
    )
    db.add(admin)
else:
    admin.role = "admin"
    admin.subscription_status = "active"
    admin.subscription_plan = "enterprise"
    admin.hashed_password = get_password_hash(ADMIN_PASSWORD)
db.commit()
db.close()

app = FastAPI(
    title="GP Project API",
    description="My awesome API with Authentication",
    version="1.0.0"
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gp-project-ruddy.vercel.app",
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https://cdn.jsdelivr.net; "
            "connect-src 'self' http://localhost:* https://*.stripe.com https://*.ngrok-free.dev https://*.vercel.app; "
            "frame-src https://*.stripe.com; "
        )
        return response

app.add_middleware(CSPMiddleware)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(items.router)
app.include_router(auth.router)
app.include_router(templates.router)
app.include_router(notes.router)
app.include_router(categories.router)
app.include_router(password_reset.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to GP Project API", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "server": "running"}

@app.get("/seed-all")
def seed_all(current_user: User = Depends(get_current_admin)):
    """Admin only: Seed new templates that don't exist. Never overwrites existing."""
    import importlib
    import os
    results = []
    
    seed_files = sorted([f.replace('.py', '') for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')])
    
    for seed_name in seed_files:
        try:
            mod = importlib.import_module(seed_name)
            for attr in dir(mod):
                if attr.startswith('seed_') and callable(getattr(mod, attr)):
                    getattr(mod, attr)()
                    results.append(f"✅ {seed_name}")
                    break
        except Exception as e:
            results.append(f"❌ {seed_name}: {str(e)[:50]}")
    
    return {"results": results}

@app.post("/change-password")
def change_password(username: str, old_password: str, new_password: str):
    from app.database import SessionLocal
    from app.models import User
    from app.auth import get_password_hash, verify_password
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"error": "User not found"}
    if not verify_password(old_password, user.hashed_password):
        return {"error": "Old password is incorrect"}
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return {"message": "Password changed successfully!"}

@app.get("/public/templates")
def public_templates():
    from app.database import SessionLocal
    from app.models import Template
    db = SessionLocal()
    templates = db.query(Template).filter(Template.is_public == True).limit(101).all()
    titles = [t.title for t in templates]
    db.close()
    return {"data": titles}

TEMPLATE_VERSION = "1.0"

@app.get("/api/template-version")
def template_version():
    return {"version": TEMPLATE_VERSION, "total_templates": 107}

@app.get("/api/sync-templates")
def sync_templates(current_user: User = Depends(get_current_admin)):
    """Admin only: Reports template count. Use /seed-all to add new templates."""
    from app.database import SessionLocal
    from app.models import Template
    
    db = SessionLocal()
    existing_count = db.query(Template).count()
    db.close()
    
    return {
        "synced": 0,
        "version": TEMPLATE_VERSION,
        "message": f"✅ {existing_count} templates in database. Use /seed-all to add new templates."
    }

@app.get("/fix-user-activity")
def fix_user_activity():
    from app.database import SessionLocal, engine
    from app.models import UserActivity
    from sqlalchemy import text
    
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='user_activities'"))
        table_exists = result.fetchone() is not None
        if table_exists:
            db.execute(text("DROP TABLE user_activities"))
            db.commit()
        UserActivity.__table__.create(engine, checkfirst=True)
        return {"message": "✅ UserActivity table fixed successfully!"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/public-test")
def public_test():
    return {"message": "Backend is reachable!", "status": "ok"}

@app.get("/public-categories")
def public_categories():
    try:
        from app.database import SessionLocal
        from app.models import Category, Template
        db = SessionLocal()
        categories = db.query(Category).all()
        result = []
        for cat in categories:
            count = db.query(Template).filter(Template.category == cat.name).count()
            result.append({"name": cat.name, "template_count": count, "id": cat.id})
        db.close()
        return {"categories": result}
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/cleanup-duplicates")
def cleanup_duplicates():
    from app.database import SessionLocal
    from app.models import Template, UserActivity, TemplateVersion, user_favourites
    from sqlalchemy import func
    db = SessionLocal()
    try:
        duplicates = db.query(Template.title, func.count(Template.id).label('count')).group_by(Template.title).having(func.count(Template.id) > 1).all()
        if not duplicates:
            return {"message": "✅ No duplicates found!", "deleted": 0}
        total_deleted = 0
        for title, count in duplicates:
            copies = db.query(Template).filter(Template.title == title).order_by(Template.view_count.desc(), Template.updated_at.desc()).all()
            for template in copies[1:]:
                db.query(UserActivity).filter(UserActivity.template_id == template.id).delete()
                db.query(TemplateVersion).filter(TemplateVersion.template_id == template.id).delete()
                db.execute(user_favourites.delete().where(user_favourites.c.template_id == template.id))
                db.delete(template)
                total_deleted += 1
        db.commit()
        return {"message": f"✅ Deleted {total_deleted} duplicate templates"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/public/templates-with-ids")
def public_templates_with_ids():
    from app.database import SessionLocal
    from app.models import Template
    db = SessionLocal()
    templates = db.query(Template).filter(Template.is_public == True).all()
    result = [{"id": t.id, "title": t.title, "category": t.category} for t in templates]
    db.close()
    return {"data": result, "total": len(result)}

@app.get("/add-references-column-render")
def add_references_column_render():
    from app.database import engine
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE templates ADD COLUMN IF NOT EXISTS clinical_references TEXT"))
            conn.commit()
        return {"message": "✅ clinical_references column added on Render"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/add-references-urti")
def add_references_urti():
    import json
    from app.database import SessionLocal
    from app.models import Template
    db = SessionLocal()
    t = db.query(Template).filter(Template.id == 841).first()
    if t:
        t.clinical_references = json.dumps([
            {"label": "HSE URTI Guidelines", "url": "https://www.hse.ie/eng/health/az/u/upper-respiratory-tract-infection/"},
            {"label": "NICE NG120 - Cough (Acute)", "url": "https://www.nice.org.uk/guidance/ng120"},
            {"label": "Heidi Evidence - URTI", "url": "https://app.heidi-app.com/search?q=URTI"}
        ])
        db.commit()
        db.close()
        return {"message": "✅ References added to URTI (ID 841)"}
    db.close()
    return {"error": "Template not found"}