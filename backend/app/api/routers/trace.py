from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.attribution.models import TraceResult
from app.attribution.path_engine import AttributionOrchestrator
from app.evidence.merkle import MerkleEngine, MerkleProof
from app.evidence.sealer import EvidenceSealer
from app.evidence.dossier import DossierGenerator
from app.sahyog.connector import MockSahyogConnector, DispatchResult

router = APIRouter()

class TraceResponse(BaseModel):
    trace_id: str
    status: str
    vasp_node: str | None
    confidence: float
    dossier_url: str
    dispatch_result: DispatchResult

@router.post("/cases/{case_id}/trace", response_model=TraceResponse)
def trigger_trace(case_id: str):
    """
    Triggers full pipeline: ingest \u2192 classify \u2192 attribute \u2192 seal \u2192 generate dossier \u2192 dispatch mock
    """
    # 1. Ingest/Classify/Attribute
    orchestrator = AttributionOrchestrator()
    # Mocking graph data for the endpoint
    seed = f"seed_{case_id}"
    vasp = "vasp_exchange"
    edges = [(seed, "hop1"), ("hop1", vasp)]
    vasp_nodes = {vasp}
    node_degrees = {seed: 1, "hop1": 2, vasp: 1}
    
    trace_result = orchestrator.trace(seed, edges, vasp_nodes, node_degrees, use_dijkstra=False)
    
    # 2. Merkle Proofs (Mocking tx hashes for the edges)
    # Tx1: seed -> hop1, Tx2: hop1 -> vasp
    tx1 = "tx_hash_1"
    tx2 = "tx_hash_2"
    block_txs = [tx1, tx2, "other_1", "other_2"]
    
    proof1 = MerkleEngine.build_proof(tx1, block_txs)
    proof2 = MerkleEngine.build_proof(tx2, block_txs)
    
    # 3. Sealer
    sealer = EvidenceSealer()
    sealed = sealer.seal(trace_result, [proof1, proof2], rng_seed="static_seed")
    
    # 4. Dossier
    dossier_gen = DossierGenerator()
    dossier_path = dossier_gen.generate_dossier(
        case_ref=case_id,
        fir_num=f"FIR-{case_id}",
        io_desig="Insp. Ramesh",
        evidence=sealed
    )
    
    # 5. SAHYOG Dispatch
    connector = MockSahyogConnector()
    dispatch_result = connector.dispatch_disclosure_request(case_id, trace_result, dossier_path)
    
    return TraceResponse(
        trace_id=sealed.snapshot_id,
        status="COMPLETED",
        vasp_node=trace_result.vasp_node,
        confidence=trace_result.confidence_result.score,
        dossier_url=dossier_path,
        dispatch_result=dispatch_result
    )
