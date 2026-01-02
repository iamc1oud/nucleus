from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Query
import secrets
from datetime import timedelta, datetime

router = APIRouter()

# TEMP: in-memory storage (replace with DB)
AUTHORIZATION_CODES = {}

@router.get("/authorize")
def authorize(
    response_type: str = Query(..., description="Response type"),
    client_id: str = Query(..., description="Client ID"),
    redirect_uri: str = Query(..., description="Redirect URI"),
    scope: str = Query(..., description="Scope"),
    state: str = Query(..., description="State"),
    code_challenge: str = Query(..., description="Code challenge"),
    code_challenge_method: str = Query(..., description="Code challenge method"),
):
    if response_type != "code":
        raise HTTPException(status_code=400, detail="unsupported_response_type")

    if code_challenge_method != "S256":
        raise HTTPException(status_code=400, detail="unsupported_code_challenge_method")

    scopes = scope.split()

    if "openid" not in scopes:
        raise HTTPException(status_code=400, detail="missing_openid_scope")

    if client_id != "forms-web":
        raise HTTPException(status_code=400, detail="invalid_client")

    # User stub
    user_id = "dev-user-1"

    code = secrets.token_urlsafe(32)

    AUTHORIZATION_CODES[code] = {
        "client_id": client_id,
        "user_id": user_id,
        "scopes": scopes,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
        "redirect_uri": redirect_uri,
        "expires_at": datetime.now() + timedelta(minutes=5)
    }

    redirect_uri = f"{redirect_uri}?code={code}"

    if state:
        redirect_uri += f"&state={state}"

    return RedirectResponse(redirect_uri)
