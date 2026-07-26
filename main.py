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
    print("No templates found. Auto-seeding all 101 templates...")
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
admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
if not admin:
    admin = User(
        username="gpclinicaldirector@notebuilder",
        email="admin@gpnotebuilder.com",
        hashed_password=get_password_hash("@GPLenovo!notes"),
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
    admin.hashed_password = get_password_hash("@GPLenovo!notes")
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
    allow_origins=["*"],
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
    return {"version": TEMPLATE_VERSION, "total_templates": 101}

@app.get("/admin/sync-templates")
def sync_templates():
    import importlib, os
    global TEMPLATE_VERSION
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
    TEMPLATE_VERSION = str(float(TEMPLATE_VERSION) + 0.1)
    return {"synced": len(results), "version": TEMPLATE_VERSION}