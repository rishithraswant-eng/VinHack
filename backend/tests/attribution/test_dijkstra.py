import pytest
from app.attribution.dijkstra import DijkstraDecayEngine

def test_dijkstra_decay_weighting():
    engine = DijkstraDecayEngine(decay_lambda=0.1)
    
    edges_temporal = [
        ("seed", "hop1", 10.0),
        ("hop1", "vasp1", 50.0), # delta t = 40 (long delay, higher decay penalty)
        ("seed", "hop2", 10.0),
        ("hop2", "vasp2", 12.0)  # delta t = 2 (short delay, lower penalty, preferred)
    ]
    vasp_nodes = {"vasp1", "vasp2"}
    
    path, vasp = engine.compute_trace("seed", edges_temporal, vasp_nodes)
    
    # Should prefer vasp2 because the time delta is smaller, meaning the decay cost is lower
    assert vasp == "vasp2"
    assert path == ["seed", "hop2", "vasp2"]
