from functools import lru_cache
import os
from fastapi import FastAPI
import psycopg2
from .config import settings

# APIs
from .api.oidc import router as oidc_router
from .api.jwks import router as jwks_router

app = FastAPI(title="Nucleus Auth Service")

app.include_router(oidc_router)
app.include_router(jwks_router)

def test_db():
    setting = get_settings()
    conn = psycopg2.connect(
        host=setting.DB_HOST,
        port=setting.DB_PORT,
        dbname=setting.DB_NAME,
        user=setting.DB_USER,
        password=setting.DB_PASSWORD
    )

    conn.close()

@lru_cache
def get_settings():
    return settings.Settings()

@app.on_event("startup")
def startup():
    test_db()

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
