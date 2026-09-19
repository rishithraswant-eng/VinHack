from typing import List, Optional
from pydantic import BaseModel

class ConfidenceResult(BaseModel):
    score: float
    ci_low: float
    ci_high: float
    requires_review: bool

class TraceResult(BaseModel):
    path: List[str]
    vasp_node: Optional[str]
    hop_count: int
    algorithm_used: str
    classifier_version: str
    confidence_result: ConfidenceResult
