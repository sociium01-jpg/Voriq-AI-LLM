import sys
import os
sys.path.insert(0, os.path.abspath("services/api-gateway"))

import pytest
from auth import hash_password, verify_password, create_access_token
import jwt

def test_password_hashing():
    raw_password = "mySecretPassword123"
    hashed = hash_password(raw_password)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("wrongPassword", hashed) is False

def test_jwt_token_generation():
    payload = {"sub": "user_123", "email": "admin@vorik.ai", "role": "super_admin"}
    token = create_access_token(payload)
    assert isinstance(token, str)
    assert len(token) > 20
