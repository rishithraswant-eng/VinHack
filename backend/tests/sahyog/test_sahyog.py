import pytest
from app.sahyog.connector import MockSahyogConnector, SahyogConnector
from app.attribution.models import TraceResult, ConfidenceResult

def test_mock_sahyog_connector():
    connector = MockSahyogConnector()
    trace = TraceResult(
        path=[], vasp_node="v", hop_count=0, algorithm_used="A", classifier_version="1",
        confidence_result=ConfidenceResult(score=1.0, ci_low=1.0, ci_high=1.0, requires_review=False)
    )
    
    result = connector.dispatch_disclosure_request("case1", trace, "path/dossier.pdf")
    
    assert result.status == "MOCK"
    assert result.labelled_mock is True
    assert result.reference_id is not None
    
def test_real_sahyog_connector():
    connector = SahyogConnector()
    trace = TraceResult(
        path=[], vasp_node="v", hop_count=0, algorithm_used="A", classifier_version="1",
        confidence_result=ConfidenceResult(score=1.0, ci_low=1.0, ci_high=1.0, requires_review=False)
    )
    
    with pytest.raises(NotImplementedError) as exc:
        connector.dispatch_disclosure_request("case1", trace, "path")
        
    assert "SAHYOG real connector not yet authorised" in str(exc.value)
