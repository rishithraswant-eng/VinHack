import logging

from app.ml.classifier import GraphClassifier, NodeClassification


def test_classifier_schema_and_audit(caplog):
    classifier = GraphClassifier(model_version="test_v1.0")
    
    mock_context = {
        "nodes": [{"id": "addrA", "type": "EOA"}],
        "edges": []
    }
    
    with caplog.at_level(logging.INFO):
        result = classifier.classify_node(address="addrA", chain="ethereum", graph_context=mock_context)
        
        # Verify schema
        assert isinstance(result, NodeClassification)
        assert hasattr(result, 'label')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'model_version')
        assert hasattr(result, 'feature_vector')
        
        # Verify audit log
        assert "AUDIT LOG: Node classified" in caplog.text
        assert "addrA" in caplog.text
        assert "ethereum" in caplog.text
        assert result.label in caplog.text
