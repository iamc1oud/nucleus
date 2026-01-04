from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def hash_password(password: str) -> str:
    """
    Encrypt the password
    """
    return ph.hash(password)

def verify_password(hash: str, password: str) -> bool:
    """
    Verify password against hashed stored value.
    """
    try:
        return ph.verify(hash, password)
    except VerifyMismatchError:
        return False