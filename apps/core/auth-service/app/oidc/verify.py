import jwt
from jwt import PyJWKClient
from app.config.settings import Settings

settings = Settings()

jwk_client = PyJWKClient(f"{settings.JWKS_URL}")

def verify_access_token(token: str) -> dict:
    signing_key = jwk_client.get_signing_key_from_jwt(token)

    claims = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=None,
        issuer=settings.ISSUER,
        options={
            "verify_aud": False
        }
    )

    return claims
