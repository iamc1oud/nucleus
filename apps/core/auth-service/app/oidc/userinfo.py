from fastapi import APIRouter, Header, HTTPException
from app.oidc.verify import verify_access_token

router = APIRouter()

@router.get("/userinfo")
def userinfo(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="invalid_authorization_header")

    token = authorization.split(" ")[1]

    try:
        claims = verify_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="invalid_token")

    scope = claims.get("scope", "")
    scopes = scope.split()

    response = {
        "sub": claims["sub"]
    }

    if "email" in scopes:
        response["email"] = "dev@nucleus.local"
        response["email_verified"] = True

    if "profile" in scopes:
        response["name"] = "Dev User"

    return response
