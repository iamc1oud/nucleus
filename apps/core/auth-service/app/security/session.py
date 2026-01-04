from fastapi import Cookie, HTTPException
from itsdangerous import URLSafeTimedSerializer

SESSION_SECRET = "CHANGE_ME"
SESSION_SALT = "session"

serializer = URLSafeTimedSerializer(SESSION_SECRET, salt=SESSION_SALT)

def create_session(user_id: str) -> str:
    return serializer.dumps({"sub": user_id})


def verify_session(token: str, max_age: int = 3600):
    return serializer.loads(token, max_age)


def get_current_user(nucelus_session: str = Cookie(None)):
    if not nucelus_session:
        raise HTTPException(status_code=401, detail="login_required")
    
    try:
        payload = verify_session(nucelus_session)
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="invalid_session")