
from pydantic import BaseModel


class ConfidenceResult(BaseModel):
    score: float
    ci_low: float
    ci_high: float
    requires_review: bool

class TraceResult(BaseModel):
    path: list[str]
    vasp_node: str | None
    hop_count: int
    algorithm_used: str
    classifier_version: str
    confidence_result: ConfidenceResult
