from fastapi import APIRouter, Form, HTTPException, Depends
from sqlmodel import Session, select
from datetime import datetime, timedelta

from ..oauth.helper import verify_pkce, sign_jwt
from ..database import get_session
from ..models.oauth import AuthorizationCode
from ..config.settings import Settings

router = APIRouter()

@router.post("/token")
def token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(...),
    code_verifier: str = Form(...),
    session: Session = Depends(get_session),
    settings: Settings = Settings()
):
    if grant_type != "authorization_code":
        raise HTTPException(status_code=400, detail="unsupported_grant_type")

    # Query authorization code from database
    statement = select(AuthorizationCode).where(
        AuthorizationCode.code == code,
        AuthorizationCode.used == False
    )
    auth_code = session.exec(statement).first()

    if not auth_code:
        raise HTTPException(status_code=400, detail="invalid_code")

    if auth_code.client_id != client_id:
        raise HTTPException(status_code=400, detail="invalid_client")

    if auth_code.redirect_uri != redirect_uri:
        raise HTTPException(status_code=400, detail="invalid_redirect_uri")

    if auth_code.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="code_expired")

    if not verify_pkce(code_verifier, auth_code.code_challenge):
        raise HTTPException(status_code=400, detail="invalid_pkce")

    # Mark code as used
    auth_code.used = True
    session.add(auth_code)
    session.commit()

    user_id = auth_code.user_id

    now = datetime.now()
    exp = now + timedelta(minutes=15)

    access_token = sign_jwt({
        "iss": settings.ISSUER,
        "sub": user_id,
        "aud": client_id,
        "scope": auth_code.scope,
        "exp": exp
    })

    id_token = sign_jwt({
        "iss": settings.ISSUER,
        "sub": user_id,
        "aud": client_id,
        "email": "dev@nucleus.local",
        "email_verified": True,
        "exp": exp
    })

    return {
        "access_token": access_token,
        "id_token": id_token,
        "token_type": "Bearer",
        "expires_in": 900
    }
