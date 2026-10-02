import os
import secrets
from authx import AuthX, AuthXConfig

from src.core.config import DATABASE_URL

import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


config = AuthXConfig()

config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or secrets.token_hex(32)
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_SECURE = False
security = AuthX(config=config)


