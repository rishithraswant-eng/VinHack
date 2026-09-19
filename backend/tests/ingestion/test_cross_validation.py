from app.ingestion.cross_validation import CrossValidator
from app.models.canonical import ValidationStatus


def test_canonical_digest():
    digest1 = CrossValidator.compute_canonical_digest(1, 100, "hash", "A", "B", "10", "BTC")
    digest2 = CrossValidator.compute_canonical_digest(1, 100, "hash", "A", "B", "10", "BTC")
    assert digest1 == digest2
    
    digest3 = CrossValidator.compute_canonical_digest(1, 100, "hash", "A", "B", "20", "BTC")
    assert digest1 != digest3

def test_cross_validation_single_source():
    validator = CrossValidator()
    responses = [
        {"canonical_digest": b"123", "data": {"value": 1}}
    ]
    status, diffs = validator.validate_responses(responses)
    assert status == ValidationStatus.SINGLE_SOURCE
    assert diffs is None

def test_cross_validation_cross_validated():
    validator = CrossValidator()
    responses = [
        {"canonical_digest": b"123", "data": {"value": 1, "fee": 10}},
        {"canonical_digest": b"123", "data": {"value": 1, "fee": 10}}
    ]
    status, diffs = validator.validate_responses(responses)
    assert status == ValidationStatus.CROSS_VALIDATED
    assert diffs is None

def test_cross_validation_conflicted():
    validator = CrossValidator()
    responses = [
        {"canonical_digest": b"123", "data": {"value": 1, "fee": 10}},
        {"canonical_digest": b"456", "data": {"value": 1, "fee": 20}}
    ]
    status, diffs = validator.validate_responses(responses)
    assert status == ValidationStatus.CONFLICTED
    assert diffs is not None
    assert "provider_0_vs_1_fee" in diffs
    assert diffs["provider_0_vs_1_fee"]["expected"] == 10
    assert diffs["provider_0_vs_1_fee"]["actual"] == 20
