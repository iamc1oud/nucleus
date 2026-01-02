import json
from fastapi import APIRouter
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

router = APIRouter()

KID = "nucleus-auth-1"

def to_base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

@router.get("/jwks.json", description="JSON Web Key Set")
def jwks():
    with open("app/keys/public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

        numbers = public_key.public_numbers()  # ty:ignore[possibly-missing-attribute]

        jwk = {
            "kty": "RSA",
            "kid": KID,
            "use": "sig",
            "alg": "RS256",
            "n": to_base64url(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, 'big')),
            "e": to_base64url(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, 'big'))
        }
        return {"keys": [jwk]}
