import pytest
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from app.core.security import require_role, create_access_token

app = FastAPI()

@app.get("/admin", dependencies=[Depends(require_role("ADMIN"))])
def admin_endpoint():
    return {"status": "ok"}

@app.get("/supervisor", dependencies=[Depends(require_role("SUPERVISOR", "ADMIN"))])
def supervisor_endpoint():
    return {"status": "ok"}

client = TestClient(app)

def test_unauthenticated_gets_401():
    response = client.get("/admin")
    assert response.status_code == 401

def test_officer_cannot_access_admin():
    token = create_access_token(data={"sub": "user1", "role": "OFFICER"})
    response = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_supervisor_can_sign_off():
    token = create_access_token(data={"sub": "user2", "role": "SUPERVISOR"})
    response = client.get("/supervisor", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
