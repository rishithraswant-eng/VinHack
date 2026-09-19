from datetime import UTC, datetime, timedelta

import jwt
import pyotp
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECURITY_ALGORITHM = "HS256"
JWT_SECRET = "super_secret_phantasm_key_for_testing"

security_scheme = HTTPBearer(auto_error=False)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[SECURITY_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):  # noqa: B008
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_access_token(credentials.credentials)
    return payload

def require_role(*roles: str):
    def role_checker(user: dict = Depends(get_current_user)):  # noqa: B008
        user_role = user.get("role")
        if user_role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return user
    return role_checker

def verify_mfa_token(user_id: str, totp_code: str, secret: str = "JBSWY3DPEHPK3PXP") -> bool:
    """
    Mock MFA token verification for the given user.
    In reality, fetch the user's secret from the database using user_id.
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(totp_code)
