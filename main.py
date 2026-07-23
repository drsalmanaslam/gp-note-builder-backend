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

# Auto-create admin on startup
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash
db = SessionLocal()
admin = db.query(User).filter(User.username == "admin").first()
if not admin:
    admin = User(
        username="admin",
        email="admin@gpnotes.com",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        is_active=True,
        subscription_status="trialing"
    )
    db.add(admin)
    db.commit()
    print("Admin user created!")
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