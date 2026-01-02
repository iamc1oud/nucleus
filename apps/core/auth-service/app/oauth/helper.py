import hashlib
import base64
from cryptography.hazmat.primitives import serialization
import jwt
from datetime import datetime, timedelta
from app.config.settings import Settings

settings = Settings()

def verify_pkce(code_verifier: str, code_challenge: str) -> bool:
    digest = hashlib.sha256(code_verifier.encode()).digest()
    computed = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    return computed == code_challenge


def load_private_key():
    """Load the private key from the file system."""
    with open("app/keys/private.pem", "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def sign_jwt(claims: dict):
    private_key = load_private_key()

    return jwt.encode(
        claims,
        private_key,
        algorithm="RS256",
        headers={"kid": settings.KID},
    )
