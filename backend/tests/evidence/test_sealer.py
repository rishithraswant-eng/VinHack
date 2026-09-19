import pytest
import os
import shutil
from app.evidence.sealer import EvidenceSealer
from app.attribution.models import TraceResult, ConfidenceResult

def test_evidence_immutability():
    storage_dir = "tests/test_storage"
    if os.path.exists(storage_dir):
        # We need write permissions to delete it because sealer sets 0o444
        for root, dirs, files in os.walk(storage_dir):
            for f in files:
                os.chmod(os.path.join(root, f), 0o777)
        shutil.rmtree(storage_dir)
        
    sealer = EvidenceSealer(storage_dir=storage_dir)
    
    trace = TraceResult(
        path=["seed", "vasp"],
        vasp_node="vasp",
        hop_count=1,
        algorithm_used="PPR",
        classifier_version="v1",
        confidence_result=ConfidenceResult(score=0.9, ci_low=0.8, ci_high=1.0, requires_review=False)
    )
    
    # First write should succeed
    evidence = sealer.seal(trace, [], "seed123")
    
    file_path = os.path.join(storage_dir, f"{evidence.snapshot_id}.json")
    assert os.path.exists(file_path)
    
    # Attempting to overwrite by mocking a sealer with the same snapshot_id
    # We will just write to the same path to simulate an overwrite attempt
    # Since the file is read-only on OS level, standard open(w) will raise PermissionError
    with pytest.raises(PermissionError):
        with open(file_path, "w") as f:
            f.write("tampered")
            
    # Cleanup
    os.chmod(file_path, 0o777)
    shutil.rmtree(storage_dir)
