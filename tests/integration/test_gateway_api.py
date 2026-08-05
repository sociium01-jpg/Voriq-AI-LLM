import sys
import os
sys.path.insert(0, os.path.abspath("services/api-gateway"))
sys.path.insert(0, os.path.abspath("packages/schemas"))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "components" in data

def test_user_signup_and_login_flow():
    signup_data = {
        "email": "developer@vorik.ai",
        "password": "pass123Word!",
        "full_name": "Priya Sharma",
        "preferred_language": "hindi"
    }
    res = client.post("/auth/signup", json=signup_data)
    assert res.status_code == 200
    token_info = res.json()
    assert "access_token" in token_info
    assert token_info["user"]["email"] == "developer@vorik.ai"

    # Login check
    login_res = client.post("/auth/login", json={"email": "developer@vorik.ai", "password": "pass123Word!"})
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

def test_indic_language_detection():
    # Test Devanagari Hindi
    hindi_res = client.post("/language/detect?text=नमस्ते आप कैसे हैं")
    assert hindi_res.status_code == 200
    assert hindi_res.json()["detected_language"] == "hindi"
    assert hindi_res.json()["detected_script"] == "devanagari"

    # Test Romanised Hinglish
    hinglish_res = client.post("/language/detect?text=kya kar rha hai bhai")
    assert hinglish_res.status_code == 200
    assert hinglish_res.json()["detected_language"] == "hindi"
    assert hinglish_res.json()["is_romanised"] is True

    # Test Romanised Manglish
    manglish_res = client.post("/language/detect?text=enikku tomorrow meeting undu cheyyan help cheyyamo")
    assert manglish_res.status_code == 200
    assert manglish_res.json()["detected_language"] == "malayalam"
    assert manglish_res.json()["is_romanised"] is True

def test_media_and_fine_tuning_endpoints():
    # First sign up to get valid Auth token
    signup_res = client.post("/auth/signup", json={
        "email": "model_engineer@vorik.ai",
        "password": "password123",
        "full_name": "Arjun V",
        "preferred_language": "malayalam"
    })
    token = signup_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test dataset upload with Auth headers
    ds_res = client.post("/datasets/upload", headers=headers, json={
        "name": "hinglish-dialogue-v1",
        "description": "Romanised Hindi customer support dialogues",
        "language": "hindi",
        "script": "latin",
        "domain": "customer_support",
        "task_type": "code_mixed_conversation",
        "license_name": "Apache-2.0",
        "commercial_use_approved": True
    })
    assert ds_res.status_code == 200
    assert ds_res.json()["pii_scan_status"] == "passed"

    # Test model registry list
    models_res = client.get("/models/registry")
    assert models_res.status_code == 200
    assert len(models_res.json()) >= 1
