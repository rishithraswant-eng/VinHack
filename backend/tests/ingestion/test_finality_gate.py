import pytest
from app.ingestion.finality import FinalityGate
from app.models.canonical import ValidationStatus

def test_finality_gate():
    config = {
        1: 6,    # Bitcoin: 6 confs
        2: 64    # Ethereum: 64 confs
    }
    gate = FinalityGate(config)
    
    # Sub-threshold
    assert gate.evaluate(1, 3) == ValidationStatus.PENDING_FINALITY
    assert gate.evaluate(2, 10) == ValidationStatus.PENDING_FINALITY
    
    # Met threshold
    assert gate.evaluate(1, 6) == ValidationStatus.UNVERIFIED
    assert gate.evaluate(2, 100) == ValidationStatus.UNVERIFIED
    
    # Unknown chain
    assert gate.evaluate(999, 1) == ValidationStatus.UNVERIFIED
