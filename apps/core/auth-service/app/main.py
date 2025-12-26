from fastapi import FastAPI

app = FastAPI(title="Nucleus Auth Service")

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
