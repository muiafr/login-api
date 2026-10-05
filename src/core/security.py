import os
import secrets
from authx import AuthX, AuthXConfig

from src.core.config import DATABASE_URL

import hashlib
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    if stored_hash.startswith("$argon2"):
        try:
            return password_hasher.verify(stored_hash, password)
        except (InvalidHashError, VerificationError):
            return False
    # Existing SHA-256 passwords are upgraded after a successful login.
    return secrets.compare_digest(stored_hash, hashlib.sha256(password.encode()).hexdigest())


config = AuthXConfig()

config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or secrets.token_hex(32)
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_SECURE = False
security = AuthX(config=config)


