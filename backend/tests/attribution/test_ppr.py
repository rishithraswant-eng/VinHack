import pytest
from app.attribution.ppr import PPREngine

def test_ppr_absorption_and_guard():
    engine = PPREngine(high_degree_threshold=5)
    
    # Simple graph
    edges = [
        ("seed", "hop1"),
        ("hop1", "hop2"),
        ("hop2", "vasp1"),
        ("hop1", "hub"), # high degree hub
        ("hub", "vasp2")
    ]
    vasp_nodes = {"vasp1", "vasp2"}
    node_degrees = {
        "seed": 1,
        "hop1": 3,
        "hop2": 1,
        "hub": 10000, # Triggers guard
        "vasp1": 1,
        "vasp2": 1
    }
    
    path, vasp = engine.compute_trace("seed", edges, vasp_nodes, node_degrees)
    
    # Should avoid 'hub' due to high degree guard and terminate at vasp1
    assert vasp == "vasp1"
    assert path == ["seed", "hop1", "hop2", "vasp1"]
    assert "hub" not in path
