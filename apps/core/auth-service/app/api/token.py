from fastapi import APIRouter, Form, HTTPException, Query
from datetime import datetime, timedelta

from app.oauth.helper import verify_pkce, sign_jwt
from .authorize import AUTHORIZATION_CODES
from app.config.settings import Settings

router = APIRouter()


@router.post("/token")
def token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(...),
    code_verifier: str = Form(...),
    settings: Settings = Settings()
):
    if grant_type != "authorization_code":
        raise HTTPException(status_code=400, detail="unsupported_grant_type")

    auth_code = AUTHORIZATION_CODES.get(code)

    if not auth_code:
        raise HTTPException(status_code=400, detail="invalid_code")

    if auth_code["client_id"] != client_id:
            raise HTTPException(status_code=400, detail="invalid_client")

    if auth_code["redirect_uri"] != redirect_uri:
        raise HTTPException(status_code=400, detail="invalid_redirect_uri")

    if auth_code["expires_at"] < datetime.now():
        raise HTTPException(status_code=400, detail="code_expired")

    if not verify_pkce(code_verifier, auth_code["code_challenge"]):
        raise HTTPException(status_code=400, detail="invalid_pkce")

    del AUTHORIZATION_CODES[code]

    user_id = auth_code["user_id"]

    now = datetime.now()
    exp = now + timedelta(minutes=15)

    access_token = sign_jwt({
        "iss": settings.ISSUER,
        "sub": user_id,
        "aud": client_id,
        "scope": "openid profile",
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
