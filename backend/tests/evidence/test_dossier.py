import os
import shutil

from pypdf import PdfReader

from app.attribution.models import ConfidenceResult, TraceResult
from app.evidence.dossier import DossierGenerator
from app.evidence.sealer import SealedEvidence


def test_dossier_pdf_limitations_footer():
    output_dir = "tests/test_dossiers"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    generator = DossierGenerator(output_dir=output_dir)
    
    trace = TraceResult(
        path=["seed", "hop", "vasp"],
        vasp_node="vasp",
        hop_count=2,
        algorithm_used="PPR",
        classifier_version="v1.0",
        confidence_result=ConfidenceResult(score=0.95, ci_low=0.90, ci_high=1.0, requires_review=False)
    )
    
    evidence = SealedEvidence(
        snapshot_id="test_snapshot_123",
        trace_result=trace,
        merkle_proofs=[],
        rng_seed="seed",
        sealed_at="2026-09-01T00:00:00Z"
    )
    
    dossier_path = generator.generate_dossier("CASE123", "FIR123", "IO Test", evidence)
    assert os.path.exists(dossier_path)
    
    # Extract PDF and assert using pypdf
    reader = PdfReader(dossier_path)
    num_pages = len(reader.pages)
    assert num_pages > 0
    
    for page_idx in range(num_pages):
        page = reader.pages[page_idx]
        text = page.extract_text()
        
        # 1. The string "LIMITATIONS" appears
        assert "LIMITATIONS" in text, f"Page {page_idx} missing LIMITATIONS text"
        # 2. The string "Section 63" appears
        assert "Section 63" in text, f"Page {page_idx} missing Section 63 text"
        
    shutil.rmtree(output_dir)
