from datetime import datetime, timedelta
from jose import JWTError
from jose import jwt  # type: ignore[import]
from uuid import uuid4

from .config import settings

def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_SECONDS)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None