import hashlib
import json
import os
import subprocess

import pytest
from pypdf import PdfReader

from app.attribution.models import ConfidenceResult, TraceResult
from app.evidence.dossier import DossierGenerator
from app.evidence.merkle import MerkleProof
from app.evidence.sealer import SealedEvidence


def test_synthetic_dossier_content(tmp_path):
    output_dir = tmp_path / "dossiers"
    ev_dir = tmp_path / "evidence"
    output_dir.mkdir()
    ev_dir.mkdir()
    
    generator = DossierGenerator(output_dir=str(output_dir))
    
    trace = TraceResult(
        path=["seed", "hop", "vasp"],
        vasp_node="vasp",
        hop_count=2,
        algorithm_used="PPR",
        classifier_version="v1.0",
        confidence_result=ConfidenceResult(score=0.95, ci_low=0.90, ci_high=1.0, requires_review=False)
    )
    
    proof1 = MerkleProof(tx_hash="0x123abc", sibling_hashes=[], is_left_node=[], merkle_root="root_abc")
    
    evidence = SealedEvidence(
        snapshot_id="test_snap",
        trace_result=trace,
        merkle_proofs=[proof1],
        rng_seed="seed",
        sealed_at="2026-09-01T00:00:00Z"
    )
    
    ev_file = ev_dir / "test_snap.json"
    with open(ev_file, "w") as f:
        json.dump(evidence.dict(), f)
    
    case_data = {
        "authority": "Sec 94 BNSS Test",
        "police_station": "Test Station 42",
        "jurisdiction_bench": "Bench 9",
        "seed_address": "0xSeed123"
    }
    
    hop_details = [{
        "hop": 1,
        "from_addr": "seed",
        "to_addr": "hop",
        "from_label": "Seed",
        "to_label": "Hop",
        "tx_hash": "0x123abc",
        "block_number": "n/a",
        "timestamp": "n/a",
        "value_base": "n/a",
        "asset": "ETH",
        "proof_index": 0
    }]
    
    dossier_path = generator.generate_dossier(
        case_ref="CASE123", 
        fir_num="FIR123", 
        io_desig="Inspector A. Sharma (Badge #SHM-8891)", 
        evidence=evidence,
        case_data=case_data,
        hop_details=hop_details
    )
    assert os.path.exists(dossier_path)
    
    reader = PdfReader(dossier_path)
    text = " ".join([page.extract_text() for page in reader.pages])
    
    assert "LIMITATIONS" in text
    assert "Section 63" in text
    assert "Inspector A. Sharma" in text
    assert "SHM-8891" in text
    assert "FIR123" in text
    assert "Sec 94 BNSS Test" in text
    assert "Test Station 42" in text
    assert "0x123abc" in text
    assert "FAIL" in text
    assert "n/a" in text

def test_synthetic_dossier_no_badge(tmp_path):
    generator = DossierGenerator(output_dir=str(tmp_path))
    trace = TraceResult(path=["seed"], vasp_node="seed", hop_count=0, algorithm_used="", classifier_version="", confidence_result=ConfidenceResult(score=0, ci_low=0, ci_high=0, requires_review=False))
    evidence = SealedEvidence(snapshot_id="s1", trace_result=trace, merkle_proofs=[], rng_seed="", sealed_at="")
    
    dossier_path = generator.generate_dossier("C1", "F1", "Constable Kumar", evidence)
    reader = PdfReader(dossier_path)
    text = " ".join([page.extract_text() for page in reader.pages])
    assert "Constable Kumar" in text

def test_synthetic_dossier_path_traversal(tmp_path):
    generator = DossierGenerator(output_dir=str(tmp_path))
    trace = TraceResult(path=["seed"], vasp_node="seed", hop_count=0, algorithm_used="", classifier_version="", confidence_result=ConfidenceResult(score=0, ci_low=0, ci_high=0, requires_review=False))
    evidence = SealedEvidence(snapshot_id="s1", trace_result=trace, merkle_proofs=[], rng_seed="", sealed_at="")
    
    with pytest.raises(ValueError):
        generator.generate_dossier("../etc/passwd", "F1", "IO", evidence)

def test_synthetic_verify_dossier_script(tmp_path):
    tx = "0xreal_tx"
    leaf = hashlib.sha256(tx.encode("utf-8")).hexdigest()
    root = leaf
    
    ev = {
        "merkle_proofs": [{
            "tx_hash": tx,
            "merkle_root": root,
            "sibling_hashes": [],
            "is_left_node": []
        }]
    }
    
    ev_file = tmp_path / "ev.json"
    with open(ev_file, "w") as f:
        json.dump(ev, f)
        
    from pathlib import Path
    script_path = str(Path(__file__).resolve().parents[3] / "scripts" / "verify_dossier.py")
    res = subprocess.run(["python", script_path, str(ev_file)], capture_output=True, text=True, check=False)
    assert res.returncode == 0
    assert "PASS" in res.stdout
    
    # Tamper
    ev["merkle_proofs"][0]["tx_hash"] = "0xtampered"
    with open(ev_file, "w") as f:
        json.dump(ev, f)
        
    res2 = subprocess.run(["python", script_path, str(ev_file)], capture_output=True, text=True, check=False)
    assert res2.returncode == 1
    assert "FAIL" in res2.stdout
