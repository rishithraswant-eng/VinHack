import pytest
import os
from backend.app.graph.neo4j_client import neo4j_router, MockNeo4jDriver

@pytest.fixture
def mock_router():
    # Force mock mode by explicitly setting the driver
    original_driver = neo4j_router.driver
    original_is_mock = neo4j_router.is_mock
    
    neo4j_router.driver = MockNeo4jDriver()
    neo4j_router.is_mock = True
    
    yield neo4j_router
    
    # Teardown
    neo4j_router.driver = original_driver
    neo4j_router.is_mock = original_is_mock

@pytest.mark.asyncio
async def test_project_address_idempotency(mock_router):
    assert mock_router.is_mock is True
    
    address_data = {
        "pg_id": "uuid-1",
        "address_canonical": "0x123",
        "created_at": "2023-01-01T00:00:00Z",
        "is_high_degree": False
    }
    
    await mock_router.project_address(1, address_data)
    
    # Verify the query executed was a MERGE
    queries = mock_router.driver.queries_executed
    assert len(queries) == 1
    assert "MERGE (a:Address {pg_id: $pg_id})" in queries[0]["query"]
    assert queries[0]["params"]["pg_id"] == "uuid-1"

@pytest.mark.asyncio
async def test_project_transaction_idempotency(mock_router):
    tx_data = {
        "tx_hash": b"hash1",
        "pg_id": "uuid-tx",
        "block_height": 100,
        "block_timestamp": "2023-01-01T00:00:00Z"
    }
    await mock_router.project_transaction(1, tx_data)
    
    queries = mock_router.driver.queries_executed
    assert len(queries) == 1
    assert "MERGE (t:Transaction {tx_hash: $tx_hash})" in queries[0]["query"]
    assert queries[0]["params"]["pg_id"] == "uuid-tx"
