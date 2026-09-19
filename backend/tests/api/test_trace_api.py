import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.routers import trace
from unittest.mock import patch

app = FastAPI()
app.include_router(trace.router)
client = TestClient(app)

@patch("app.api.routers.trace.AttributionOrchestrator.trace")
@patch("app.api.routers.trace.MerkleEngine.build_proof")
def test_trace_api_endpoint(mock_build_proof, mock_trace):
    from app.attribution.models import TraceResult, ConfidenceResult
    
    mock_trace.return_value = TraceResult(
        path=["seed", "vasp"],
        vasp_node="vasp",
        hop_count=1,
        algorithm_used="PPR",
        classifier_version="v1",
        confidence_result=ConfidenceResult(score=0.9, ci_low=0.8, ci_high=1.0, requires_review=False)
    )
    
    from app.evidence.merkle import MerkleProof
    mock_build_proof.return_value = MerkleProof(tx_hash="t", sibling_hashes=[], is_left_node=[], merkle_root="r")
    
    response = client.post("/cases/123/trace")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert data["vasp_node"] == "vasp"
    assert "trace_id" in data
    assert "dossier_url" in data
    assert data["dispatch_result"]["status"] == "MOCK"
