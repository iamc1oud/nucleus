import os
from fastapi import FastAPI
import psycopg2

app = FastAPI(title="Nucleus Auth Service")

def test_db():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    conn.close()

@app.on_event("startup")
def startup():
    test_db()

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
