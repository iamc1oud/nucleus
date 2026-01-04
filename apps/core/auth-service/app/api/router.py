from fastapi import APIRouter

from .authorize import router as authorize_router
from .oidc import router as oidc_router
from .jwks import router as jwks_router
from .authorize import router as authorize_router
from .token import router as token_router
from .login import router as login_router

app = APIRouter()

app.include_router(oidc_router)
app.include_router(jwks_router)
app.include_router(authorize_router)
app.include_router(token_router)
app.include_router(login_router)

