import pytest
import pyotp
import time
from app.core.security import verify_mfa_token

def test_valid_totp_passes():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    code = totp.now()
    assert verify_mfa_token("user_id", code, secret=secret) is True

def test_invalid_totp_fails():
    secret = pyotp.random_base32()
    assert verify_mfa_token("user_id", "000000", secret=secret) is False

def test_expired_totp_fails():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    # Generate code for a time in the past (beyond the standard 30s window)
    code = totp.at(time.time() - 120)
    assert verify_mfa_token("user_id", code, secret=secret) is False
