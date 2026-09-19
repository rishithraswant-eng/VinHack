import pytest
from unittest.mock import patch
from app.attribution.path_engine import AttributionOrchestrator

@patch("app.ml.classifier.GraphClassifier.classify_node")
def test_path_engine_classify_first(mock_classify):
    orchestrator = AttributionOrchestrator()
    
    edges = [("seed", "vasp")]
    vasp_nodes = {"vasp"}
    node_degrees = {"seed": 1, "vasp": 1}
    
    result = orchestrator.trace("seed", edges, vasp_nodes, node_degrees, use_dijkstra=False)
    
    # Assert classify was called (enforcing classify-first)
    mock_classify.assert_called_once_with("seed", "bitcoin", {})
    
    # Assert result structure
    assert result.vasp_node == "vasp"
    assert result.algorithm_used == "PPR"
    assert result.hop_count == 1
    assert result.classifier_version == "HGT-v1.0"
    assert result.confidence_result is not None
