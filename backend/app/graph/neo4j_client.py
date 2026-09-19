import logging
from typing import Dict, Any, List, Optional
from app.core.config import settings
try:
    from neo4j import AsyncGraphDatabase, AsyncSession
except ImportError:
    pass # Will be handled if not installed, but for mock tests we'll use a MockDriver

logger = logging.getLogger(__name__)

class MockNeo4jDriver:
    def __init__(self):
        self.queries_executed = []
    
    def session(self, database=None):
        return MockNeo4jSession(self.queries_executed, database)

    async def close(self):
        pass

class MockNeo4jSession:
    def __init__(self, query_log, database):
        self.query_log = query_log
        self.database = database
    
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def run(self, query: str, **kwargs):
        self.query_log.append({
            "database": self.database,
            "query": query,
            "params": kwargs
        })
        return MockNeo4jResult()

class MockNeo4jResult:
    async def fetch(self, n):
        return []
        
    async def single(self):
        return None
        
    async def consume(self):
        return None

class Neo4jRouter:
    def __init__(self):
        if settings.NEO4J_URI.startswith("mock://"):
            self.driver = MockNeo4jDriver()
            self.is_mock = True
        else:
            self.driver = AsyncGraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            self.is_mock = False

    def get_database_for_chain(self, chain_id: int) -> str:
        # Example routing
        if chain_id == 1:
            return "shard-btc"
        elif chain_id == 2:
            return "shard-eth"
        return "shard-default"

    async def setup_constraints(self, chain_id: int):
        db = self.get_database_for_chain(chain_id)
        queries = [
            "CREATE CONSTRAINT address_id_unique IF NOT EXISTS FOR (n:Address) REQUIRE n.pg_id IS UNIQUE",
            "CREATE CONSTRAINT tx_hash_unique IF NOT EXISTS FOR (n:Transaction) REQUIRE n.tx_hash IS UNIQUE"
        ]
        async with self.driver.session(database=db) as session:
            for q in queries:
                await session.run(q)

    async def project_address(self, chain_id: int, address_data: Dict[str, Any]):
        """Idempotent MERGE projection from PostgreSQL -> Neo4j for Address"""
        db = self.get_database_for_chain(chain_id)
        query = """
        MERGE (a:Address {pg_id: $pg_id})
        ON CREATE SET 
            a.address_canonical = $address_canonical,
            a.created_at = $created_at,
            a.is_high_degree = $is_high_degree
        ON MATCH SET 
            a.is_high_degree = $is_high_degree
        """
        async with self.driver.session(database=db) as session:
            await session.run(query, **address_data)

    async def project_transaction(self, chain_id: int, tx_data: Dict[str, Any]):
        """Idempotent MERGE projection from PostgreSQL -> Neo4j for Transaction"""
        db = self.get_database_for_chain(chain_id)
        query = """
        MERGE (t:Transaction {tx_hash: $tx_hash})
        ON CREATE SET 
            t.pg_id = $pg_id,
            t.block_height = $block_height,
            t.block_timestamp = $block_timestamp
        """
        async with self.driver.session(database=db) as session:
            await session.run(query, **tx_data)

    async def project_transfer(self, chain_id: int, transfer_data: Dict[str, Any]):
        """Idempotent MERGE projection for Transfer (Edge)"""
        db = self.get_database_for_chain(chain_id)
        query = """
        MATCH (from:Address {pg_id: $from_id})
        MATCH (to:Address {pg_id: $to_id})
        MATCH (tx:Transaction {tx_hash: $tx_hash})
        MERGE (from)-[r:TRANSFERRED {pg_id: $transfer_id}]->(to)
        ON CREATE SET 
            r.value_base = $value_base,
            r.asset_id = $asset_id,
            r.block_timestamp = $block_timestamp,
            r.tx_hash = $tx_hash
        """
        async with self.driver.session(database=db) as session:
            await session.run(query, **transfer_data)

    # Q1: Tracing paths up to N hops
    async def q1_trace_paths(self, chain_id: int, seed_id: str, max_depth: int = 12):
        db = self.get_database_for_chain(chain_id)
        # high-degree node guard applied inline
        query = """
        MATCH p = (seed:Address {pg_id: $seed_id})-[r:TRANSFERRED*1..$max_depth]->(terminal:Address)
        WHERE ALL(n IN nodes(p) WHERE n.is_high_degree = false OR n = seed OR n = terminal)
        RETURN p
        LIMIT 100
        """
        async with self.driver.session(database=db) as session:
            return await session.run(query, seed_id=seed_id, max_depth=max_depth)

    # Q2: Shortest path between two addresses
    async def q2_shortest_path(self, chain_id: int, src_id: str, dst_id: str, max_depth: int = 12):
        db = self.get_database_for_chain(chain_id)
        query = """
        MATCH p = shortestPath((src:Address {pg_id: $src_id})-[*1..$max_depth]-(dst:Address {pg_id: $dst_id}))
        WHERE ALL(n IN nodes(p) WHERE n.is_high_degree = false OR n IN [src, dst])
        RETURN p
        """
        async with self.driver.session(database=db) as session:
            return await session.run(query, src_id=src_id, dst_id=dst_id, max_depth=max_depth)

    # Q3: Common spenders/receivers
    async def q3_common_counterparties(self, chain_id: int, addresses: List[str]):
        db = self.get_database_for_chain(chain_id)
        query = """
        UNWIND $addresses AS addr_id
        MATCH (a:Address {pg_id: addr_id})-[:TRANSFERRED]->(counterparty:Address)
        WHERE counterparty.is_high_degree = false
        WITH counterparty, count(DISTINCT a) AS matched_seeds
        WHERE matched_seeds = size($addresses)
        RETURN counterparty
        """
        async with self.driver.session(database=db) as session:
            return await session.run(query, addresses=addresses)

    # Q4: Bridge traversal (simulated via BridgeStub nodes or cross-shard query)
    async def q4_bridge_traversal(self, src_chain: int, bridge_pg_id: str):
        db = self.get_database_for_chain(src_chain)
        query = """
        MATCH (a:Address)-[:TRANSFERRED]->(b:BridgeStub {bridge_index_id: $bridge_pg_id})
        RETURN a
        """
        async with self.driver.session(database=db) as session:
            return await session.run(query, bridge_pg_id=bridge_pg_id)

neo4j_router = Neo4jRouter()
