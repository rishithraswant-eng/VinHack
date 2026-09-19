import os
import uuid
from datetime import UTC, datetime

from pydantic import BaseModel

from app.attribution.models import TraceResult
from app.evidence.merkle import MerkleProof


class SealedEvidence(BaseModel):
    snapshot_id: str
    trace_result: TraceResult
    merkle_proofs: list[MerkleProof]
    rng_seed: str
    sealed_at: str

class EvidenceSealer:
    def __init__(self, storage_dir: str = "storage/evidence"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        
    def seal(self, trace_result: TraceResult, merkle_proofs: list[MerkleProof], rng_seed: str) -> SealedEvidence:
        evidence = SealedEvidence(
            snapshot_id=str(uuid.uuid4()),
            trace_result=trace_result,
            merkle_proofs=merkle_proofs,
            rng_seed=rng_seed,
            sealed_at=datetime.now(UTC).isoformat()
        )
        
        file_path = os.path.join(self.storage_dir, f"{evidence.snapshot_id}.json")
        
        if os.path.exists(file_path):
            raise FileExistsError("Immutability violation: Sealed evidence already exists at this path.")
            
        with open(file_path, "w") as f:
            f.write(evidence.model_dump_json(indent=2))
            
        # Protect file logic (simulate immutability guard)
        # In actual system, object store handles immutable versions/locks
        # Make file read-only on local disk
        os.chmod(file_path, 0o444)
        
        return evidence
