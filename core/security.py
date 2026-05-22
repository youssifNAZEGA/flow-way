import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import hashlib

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def hash_password(password: str) -> str:
    # Use SHA256 first to avoid bcrypt's 72-character limit
    # and then salt/hash with bcrypt
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw_hash.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return bcrypt.checkpw(pw_hash.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(username: str):
    payload = {
        "sub": username,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(username: str):
    payload = {
        "sub": username,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_token(username: str):
    # Backward compatibility
    return create_access_token(username)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
