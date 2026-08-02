from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import categories, notes
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import users, products, items, auth, templates
from app.database import engine, Base
import os

# Create tables
Base.metadata.create_all(bind=engine)

# Auto-seed templates on first startup (only if database is empty)
from app.database import SessionLocal
from app.models import Template
import importlib
import os

db_check = SessionLocal()
existing_templates = db_check.query(Template).count()
db_check.close()

if existing_templates == 0:
    print("No templates found. Auto-seeding all 107 templates...")
    seed_files = sorted([f.replace('.py', '') for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')])
    for seed_name in seed_files:
        try:
            mod = importlib.import_module(seed_name)
            for attr in dir(mod):
                if attr.startswith('seed_') and callable(getattr(mod, attr)):
                    getattr(mod, attr)()
                    break
        except Exception as e:
            print(f"❌ {seed_name}: {str(e)[:50]}")
    print("Auto-seeding complete!")
else:
    print(f"{existing_templates} templates already exist. Skipping seed.")

# Ensure admin has lifetime access
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash
db = SessionLocal()

import os
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

@app.get("/")
def read_root():
    return {"message": "Welcome to GP Project API", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "server": "running"}

@app.get("/seed-all")
def seed_all():
    import importlib
    import os
    results = []
    
    # Get all seed files
    seed_files = sorted([f.replace('.py', '') for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')])
    
    for seed_name in seed_files:
        try:
            mod = importlib.import_module(seed_name)
            # Find the seed function (usually starts with seed_)
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

# Template version tracking
TEMPLATE_VERSION = "1.0"  # Increment this when you update seeds

@app.get("/api/template-version")
def template_version():
    return {"version": TEMPLATE_VERSION, "total_templates": 107}

@app.get("/api/sync-templates")
def sync_templates():
    import importlib, os
    global TEMPLATE_VERSION
    from app.database import SessionLocal
    from app.models import Template
    from datetime import datetime, timezone
    
    db = SessionLocal()
    
    # Get existing template titles - ONLY sync if no templates exist (first run)
    existing_count = db.query(Template).count()
    
    if existing_count > 0:
        db.close()
        return {
            "synced": 0,
            "version": TEMPLATE_VERSION,
            "message": f"✅ {existing_count} templates already exist. Skipping sync to preserve edits."
        }
    
    print(f"📊 No templates found. Running initial seed...")
    
    results = []
    added_count = 0
    
    seed_files = sorted([f.replace('.py', '') for f in os.listdir('.') if f.startswith('seed_') and f.endswith('.py')])
    
    for seed_name in seed_files:
        try:
            mod = importlib.import_module(seed_name)
            for attr in dir(mod):
                if attr.startswith('seed_') and callable(getattr(mod, attr)):
                    # Run the seed function - only runs when database is empty
                    getattr(mod, attr)()
                    results.append(f"✅ {seed_name}")
                    added_count += 1
                    break
        except Exception as e:
            results.append(f"❌ {seed_name}: {str(e)[:50]}")
    
    db.close()
    TEMPLATE_VERSION = str(float(TEMPLATE_VERSION) + 0.1)
    
    return {
        "synced": added_count,
        "version": TEMPLATE_VERSION,
        "message": f"Initial seeding complete - {added_count} templates added.",
        "details": results[:5]  # Show first 5 results for debugging
    }

@app.get("/fix-user-activity")
def fix_user_activity():
    from app.database import SessionLocal, engine
    from app.models import UserActivity
    from sqlalchemy import text
    
    db = SessionLocal()
    
    try:
        # SQLite check - see if table exists
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='user_activities'"))
        table_exists = result.fetchone() is not None
        
        if table_exists:
            # Drop the table
            db.execute(text("DROP TABLE user_activities"))
            db.commit()
            print("✅ Dropped existing user_activities table")
        
        # Recreate the table
        UserActivity.__table__.create(engine, checkfirst=True)
        print("✅ Recreated user_activities table with primary key")
        
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
            # Count templates directly from the Template table
            count = db.query(Template).filter(Template.category == cat.name).count()
            result.append({
                "name": cat.name,
                "template_count": count,
                "id": cat.id
            })
        db.close()
        return {"categories": result}
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/add-template-count-column")
def add_template_count_column():
    try:
        from app.database import engine
        from sqlalchemy import text
        
        # Use the engine's connection directly
        with engine.connect() as conn:
            # Try to add the column using SQLAlchemy's built-in method
            try:
                # For SQLite
                conn.execute(text("ALTER TABLE categories ADD COLUMN template_count INTEGER DEFAULT 0"))
                conn.commit()
                return {"message": "✅ Column added successfully"}
            except Exception as e:
                # Check if column already exists
                result = conn.execute(text("PRAGMA table_info(categories)"))
                columns = [row[1] for row in result]
                if 'template_count' in columns:
                    return {"message": "✅ Column already exists"}
                else:
                    return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/public-categories")
def public_categories():
    try:
        from app.database import SessionLocal
        from app.models import Category, Template
        
        db = SessionLocal()
        categories = db.query(Category).all()
        result = []
        for cat in categories:
            # Count templates directly from the Template table
            count = db.query(Template).filter(Template.category == cat.name).count()
            result.append({
                "name": cat.name,
                "template_count": count,
                "id": cat.id
            })
        db.close()
        return {"categories": result}
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/fix-template-count")
def fix_template_count():
    import sqlite3
    import os
    
    try:
        db_path = os.environ.get('DATABASE_URL', 'gp_notes.db')
        if db_path and db_path.startswith('sqlite:///'):
            db_path = db_path.replace('sqlite:///', '')
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(categories)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'template_count' not in columns:
            cursor.execute("ALTER TABLE categories ADD COLUMN template_count INTEGER DEFAULT 0")
            conn.commit()
            result = {"message": "✅ Added template_count column"}
        else:
            result = {"message": "✅ Column already exists"}
        
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/fix-render-db")
def fix_render_db():
    import sqlite3
    import os
    
    db_path = os.environ.get('DATABASE_URL', 'gp_notes.db')
    
    if db_path and db_path.startswith('sqlite:///'):
        db_path = db_path.replace('sqlite:///', '')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(categories)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'template_count' not in columns:
            cursor.execute("ALTER TABLE categories ADD COLUMN template_count INTEGER DEFAULT 0")
            conn.commit()
            return {"message": "✅ Column added successfully to Render database!"}
        else:
            return {"message": "✅ Column already exists!"}
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/cleanup-duplicates")
def cleanup_duplicates():
    """Remove duplicate templates - keep the one with highest view_count"""
    from app.database import SessionLocal
    from app.models import Template, UserActivity, TemplateVersion, user_favourites
    from sqlalchemy import func
    
    db = SessionLocal()
    
    try:
        # Find duplicate titles
        duplicates = db.query(
            Template.title, 
            func.count(Template.id).label('count')
        ).group_by(Template.title).having(func.count(Template.id) > 1).all()
        
        if not duplicates:
            return {"message": "✅ No duplicates found!", "deleted": 0}
        
        total_deleted = 0
        results = []
        
        for title, count in duplicates:
            copies = db.query(Template).filter(Template.title == title).order_by(
                Template.view_count.desc(), 
                Template.updated_at.desc()
            ).all()
            
            keep = copies[0]
            results.append(f"Title: '{title}' - Keeping ID={keep.id} (views={keep.view_count})")
            
            for template in copies[1:]:
                # Delete related records first
                db.query(UserActivity).filter(UserActivity.template_id == template.id).delete()
                db.query(TemplateVersion).filter(TemplateVersion.template_id == template.id).delete()
                db.execute(user_favourites.delete().where(user_favourites.c.template_id == template.id))
                
                # Now delete the template
                db.delete(template)
                results.append(f"  Deleted ID={template.id} (views={template.view_count})")
                total_deleted += 1
        
        db.commit()
        return {
            "message": f"✅ Deleted {total_deleted} duplicate templates",
            "details": results
        }
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