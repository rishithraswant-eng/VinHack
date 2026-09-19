import pytest
from app.attribution.monte_carlo import MonteCarloScorer

def test_monte_carlo_confidence():
    scorer = MonteCarloScorer(num_walks=100, threshold=0.95)
    
    path = ["seed", "hop", "vasp"]
    
    result = scorer.compute_confidence(path, "vasp", [])
    
    # Score should be between 0 and 1
    assert 0.0 <= result.score <= 1.0
    assert 0.0 <= result.ci_low <= 1.0
    assert 0.0 <= result.ci_high <= 1.0
    
    # Because we mocked hit rate to ~0.8 and set threshold to 0.95, it should require review
    assert result.requires_review is True
