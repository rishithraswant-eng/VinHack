from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routers import trace

app = FastAPI()
app.include_router(trace.router)
client = TestClient(app)

@patch("app.api.routers.trace.AttributionOrchestrator.trace")
@patch("app.api.routers.trace.MerkleEngine.build_proof")
def test_trace_api_endpoint(mock_build_proof, mock_trace):
    
    response = client.post("/traces/", json={"case_id": "123", "seed_address": "abc"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "PENDING"
    assert "trace_id" in data
