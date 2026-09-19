import pytest
import logging
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from app.core.audit_middleware import AuditMiddleware

app = FastAPI()
app.add_middleware(AuditMiddleware)

@app.get("/cases/123/view")
def view_case():
    return {"status": "ok"}

@app.post("/cases/123/update")
def update_case():
    return {"status": "ok"}

client = TestClient(app)

def test_audit_middleware(caplog):
    caplog.set_level(logging.INFO)
    
    # GET request should not emit audit event
    response = client.get("/cases/123/view")
    assert response.status_code == 200
    
    audit_logs = [r for r in caplog.records if "AUDIT EVENT" in r.getMessage()]
    assert len(audit_logs) == 0
    
    # POST request should emit audit event
    response = client.post("/cases/123/update")
    assert response.status_code == 200
    
    audit_logs = [r for r in caplog.records if "AUDIT EVENT" in r.getMessage()]
    assert len(audit_logs) == 1
    
    log_msg = audit_logs[0].getMessage()
    assert "'method': 'POST'" in log_msg
    assert "'case_id': '123'" in log_msg
    assert "'endpoint': '/cases/123/update'" in log_msg
