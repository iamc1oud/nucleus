from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
import secrets
from datetime import timedelta, datetime

from ..database import get_session
from ..models.oauth import AuthorizationCode
from ..security.session import get_current_user

router = APIRouter()

@router.get("/authorize")
def authorize(
    response_type: str = Query(..., description="Response type"),
    client_id: str = Query(..., description="Client ID"),
    redirect_uri: str = Query(..., description="Redirect URI"),
    scope: str = Query(..., description="Scope"),
    state: str = Query(..., description="State"),
    code_challenge: str = Query(..., description="Code challenge"),
    code_challenge_method: str = Query(..., description="Code challenge method"),
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
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

    code = secrets.token_urlsafe(32)

    # Create authorization code in database
    auth_code = AuthorizationCode(
        code=code,
        client_id=client_id,
        user_id=user_id,
        scope=" ".join(scopes),
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        redirect_uri=redirect_uri,
        expires_at=datetime.now() + timedelta(minutes=5)
    )
    
    session.add(auth_code)
    session.commit()

    redirect_uri = f"{redirect_uri}?code={code}"

    if state:
        redirect_uri += f"&state={state}"

    return RedirectResponse(redirect_uri)
