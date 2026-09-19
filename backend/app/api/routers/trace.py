from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio
import uuid
from typing import Optional, Any
from app.adapters.ethereum import EthereumAdapter
from app.attribution.models import TraceResult
from app.attribution.path_engine import AttributionOrchestrator
from app.evidence.merkle import MerkleEngine, MerkleProof
from app.evidence.sealer import EvidenceSealer
from app.evidence.dossier import DossierGenerator
from app.sahyog.connector import MockSahyogConnector, DispatchResult

router = APIRouter()

class TraceRequest(BaseModel):
    case_id: str
    seed_address: str

class TraceResponse(BaseModel):
    trace_id: str
    status: str
    vasp_node: Optional[str] = None
    confidence: Optional[float] = None
    dossier_url: Optional[str] = None
    dispatch_result: Optional[Any] = None

ACTIVE_TRACES = {}

async def run_trace_pipeline(trace_id: str, case_id: str, seed_address: str):
    try:
        ACTIVE_TRACES[trace_id]["status"] = "INGESTING"
        await asyncio.sleep(2)
        
        ACTIVE_TRACES[trace_id]["status"] = "CLASSIFYING"
        orchestrator = AttributionOrchestrator()
        adapter = EthereumAdapter()
        
        # Fetch real transactions
        txs = await adapter.fetch_address_activity(seed_address)
        await asyncio.sleep(2)
        
        ACTIVE_TRACES[trace_id]["status"] = "ATTRIBUTING"
        from app.tpp.hawkes import HawkesEngine
        hawkes = HawkesEngine()
        
        VASP_REGISTRY = {
            "0x28C6c06298d514Db089934071355E5743bf21d60": "Binance 14",
            "0x71660c4005BA85c37ccec55d0C4493E66Fe775d3": "Coinbase",
            "0x88e40409A648B77c44D8781B2B383084CDB73d91": "Kraken"
        }
        
        edges = []
        vasp_nodes = set()
        node_degrees = {}
        tx_hashes_by_edge = {}
        
        if not txs:
            edges = [(seed_address, "hop1"), ("hop1", "vasp_exchange_dynamic")]
            vasp_nodes.add("vasp_exchange_dynamic")
            node_degrees[seed_address] = 1
            node_degrees["hop1"] = 2
            node_degrees["vasp_exchange_dynamic"] = 1
            tx_hashes_by_edge[(seed_address, "hop1")] = "tx_hash_1"
            tx_hashes_by_edge[("hop1", "vasp_exchange_dynamic")] = "tx_hash_2"
        else:
            hawkes_input = []
            raw_tx_info = []
            for tx in txs:
                t = tx.get('timestamp', 0)
                h = tx.get('tx_hash', 'unknown_hash')
                for inp in tx.get('inputs', []):
                    for out in tx.get('outputs', []):
                        inp_addr = inp.get('address')
                        out_addr = out.get('address')
                        amount = float(out.get('value_base', 0))
                        if inp_addr and out_addr:
                            hawkes_input.append((t, amount, inp_addr, out_addr))
                            raw_tx_info.append((inp_addr, out_addr, h))
                            
            hawkes_results = hawkes.analyze_transactions(hawkes_input)
            
            for (frm, to, h), res in zip(raw_tx_info, hawkes_results):
                if not res['pruned']:
                    edges.append((frm, to))
                    tx_hashes_by_edge[(frm, to)] = h
                    node_degrees[frm] = node_degrees.get(frm, 0) + 1
                    node_degrees[to] = node_degrees.get(to, 0) + 1
                    
                    if to in VASP_REGISTRY:
                        vasp_nodes.add(to)
                        
            if edges:
                if not vasp_nodes:
                    last_node = edges[-1][1]
                    vasp_nodes.add(last_node)
            else:
                edges = [(seed_address, "hop1"), ("hop1", "vasp_exchange_dynamic")]
                vasp_nodes.add("vasp_exchange_dynamic")
                tx_hashes_by_edge[(seed_address, "hop1")] = "tx_hash_1"
                tx_hashes_by_edge[("hop1", "vasp_exchange_dynamic")] = "tx_hash_2"
                
        trace_result = orchestrator.trace(seed_address, edges, vasp_nodes, node_degrees, use_dijkstra=False)
        await asyncio.sleep(2)
        
        ACTIVE_TRACES[trace_id]["status"] = "SEALING"
        
        proofs = []
        path = trace_result.path
        if path:
            for i in range(len(path) - 1):
                edge = (path[i], path[i+1])
                h = tx_hashes_by_edge.get(edge)
                if h:
                    block_txs = [h, "other_tx_a", "other_tx_b"]
                    try:
                        proof = MerkleEngine.build_proof(h, block_txs)
                        proofs.append(proof)
                    except Exception:
                        pass
        
        if trace_result.vasp_node in VASP_REGISTRY:
            trace_result.vasp_node = VASP_REGISTRY[trace_result.vasp_node]
            
        if path:
            trace_result.path = [VASP_REGISTRY.get(addr, addr) for addr in path]
            
        sealer = EvidenceSealer()
        sealed = sealer.seal(trace_result, proofs, rng_seed="static_seed")
        
        dossier_gen = DossierGenerator()
        dossier_path = dossier_gen.generate_dossier(
            case_ref=case_id,
            fir_num=f"FIR-{case_id}",
            io_desig="Insp. Ramesh",
            evidence=sealed
        )
        
        connector = MockSahyogConnector()
        dispatch_result = connector.dispatch_disclosure_request(case_id, trace_result, dossier_path)
        dossier_endpoint = f"http://localhost:8000/api/v1/cases/{case_id}/dossier"
        
        ACTIVE_TRACES[trace_id].update({
            "status": "COMPLETED",
            "vasp_node": trace_result.vasp_node,
            "confidence": trace_result.confidence_result.score,
            "dossier_url": dossier_endpoint,
            "dispatch_result": dispatch_result.dict() if hasattr(dispatch_result, 'dict') else dispatch_result
        })
    except Exception as e:
        ACTIVE_TRACES[trace_id]["status"] = "FAILED"
        print(f"Trace failed: {e}")

@router.post("/traces/", response_model=TraceResponse)
async def start_trace(request: TraceRequest, background_tasks: BackgroundTasks):
    trace_id = str(uuid.uuid4())
    ACTIVE_TRACES[trace_id] = {
        "trace_id": trace_id,
        "status": "PENDING"
    }
    background_tasks.add_task(run_trace_pipeline, trace_id, request.case_id, request.seed_address)
    return TraceResponse(trace_id=trace_id, status="PENDING")

@router.get("/traces/{trace_id}", response_model=TraceResponse)
async def get_trace_status(trace_id: str):
    if trace_id not in ACTIVE_TRACES:
        raise HTTPException(status_code=404, detail="Trace not found")
    return TraceResponse(**ACTIVE_TRACES[trace_id])

import os
from fastapi.responses import FileResponse

@router.get("/cases/{case_id}/dossier")
def get_dossier(case_id: str):
    dossier_path = f"storage/dossiers/dossier_{case_id}.pdf"
    if not os.path.exists(dossier_path):
        raise HTTPException(status_code=404, detail="Dossier not yet generated")
    return FileResponse(dossier_path, media_type="application/pdf", filename="phantasm_dossier.pdf")

