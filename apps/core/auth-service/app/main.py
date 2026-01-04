from contextlib import asynccontextmanager
from functools import lru_cache
from fastapi import FastAPI, Depends
from sqlmodel import Session
from .config import settings
from .database import init_db, get_engine, get_session
from .models import AuthorizationCode  # Import models to register them
from .db_utils import cleanup_expired_codes, get_active_codes_count

# APIs
from .api.router import app as api_routes
from .oidc.userinfo import router as userinfo_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    init_db()
    print("Database initialized")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(title="Nucleus Auth Service", lifespan=lifespan)

app.include_router(api_routes)
app.include_router(userinfo_router)

@lru_cache
def get_settings():
    return settings.Settings()

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/admin/db-stats")
def db_stats():
    """Get database statistics"""
    active_codes = get_active_codes_count()
    return {
        "active_authorization_codes": active_codes
    }

@app.post("/admin/cleanup")
def cleanup_expired():
    """Clean up expired authorization codes"""
    cleaned_count = cleanup_expired_codes()
    return {
        "message": f"Cleaned up {cleaned_count} expired authorization codes"
    }
