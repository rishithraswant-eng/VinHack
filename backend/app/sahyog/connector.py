import uuid
from typing import Optional
from pydantic import BaseModel
from app.attribution.models import TraceResult

class DispatchResult(BaseModel):
    status: str
    reference_id: str
    labelled_mock: bool
    
class SahyogConnector:
    def dispatch_disclosure_request(self, case: str, trace_result: TraceResult, dossier_path: str) -> DispatchResult:
        raise NotImplementedError("SAHYOG real connector not yet authorised \u2014 OQ-01 unresolved")

class MockSahyogConnector(SahyogConnector):
    def dispatch_disclosure_request(self, case: str, trace_result: TraceResult, dossier_path: str) -> DispatchResult:
        # Log request (mocking)
        print(f"[MOCK] Dispatched SAHYOG request for case {case}. Trace to {trace_result.vasp_node}. Dossier: {dossier_path}")
        
        return DispatchResult(
            status="MOCK",
            reference_id=str(uuid.uuid4()),
            labelled_mock=True
        )
