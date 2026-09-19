from app.tpp.hawkes import HawkesEngine


def test_hawkes_normal_tx():
    engine = HawkesEngine(mu=0.1, alpha=0.5, beta=1.0)
    
    # 2 transactions, far apart
    transactions = [
        (10.0, 50000, "addrA", "addrB"),
        (100.0, 50000, "addrA", "addrC")
    ]
    
    results = engine.analyze_transactions(transactions)
    
    # Normal transactions should not be pruned
    for res in results:
        assert not res['pruned']
        assert res['noise_score'] < 1.0

def test_hawkes_bot_burst():
    engine = HawkesEngine(mu=0.1, alpha=0.5, beta=1.0)
    
    # Many transactions in a short period (burst)
    transactions = [
        (1.0, 50000, "addrA", "addrB"),
        (1.1, 50000, "addrA", "addrC"),
        (1.2, 50000, "addrA", "addrD"),
        (1.3, 50000, "addrA", "addrE"),
        (1.4, 50000, "addrA", "addrF"),
        (1.5, 50000, "addrA", "addrG"),
    ]
    
    results = engine.analyze_transactions(transactions)
    
    # At least the later ones should be pruned
    assert any(res['pruned'] for res in results)
    
def test_hawkes_peel_chain():
    engine = HawkesEngine(mu=0.1, alpha=0.5, beta=1.0)
    
    # Peel chain: quick successive transfers with similar large amounts
    transactions = [
        (10.0, 1000000, "addrA", "addrB"),
        (10.5, 999000, "addrA", "addrC"), # 1000 sat fee deducted
        (11.0, 998000, "addrA", "addrD"),
    ]
    
    results = engine.analyze_transactions(transactions)
    
    # Third one should be caught as a peel-chain pattern
    assert results[-1]['pruned']
    assert results[-1]['noise_score'] > 0.1
