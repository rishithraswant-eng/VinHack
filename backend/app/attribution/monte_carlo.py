import random

from app.attribution.models import ConfidenceResult
from app.core.config import settings


class MonteCarloScorer:
    def __init__(self, num_walks: int = settings.RWR_WALKS, threshold: float = settings.CONFIDENCE_THRESHOLD):
        self.num_walks = num_walks
        self.threshold = threshold

    def compute_confidence(self, path: list, vasp_node: str, graph_edges: list) -> ConfidenceResult:
        if not path or not vasp_node:
            return ConfidenceResult(score=0.0, ci_low=0.0, ci_high=0.0, requires_review=True)
            
        # Mocking RWR simulation for the given path
        # Real implementation would simulate random walks from seed to see how often it hits vasp_node
        hits = 0
        for _ in range(self.num_walks):
            # In mock, simulate hits with ~80% probability for direct paths
            if random.random() < 0.8:
                hits += 1
                
        score = hits / self.num_walks
        # Simple binomial confidence interval (95%)
        z = 1.96
        if self.num_walks > 0:
            margin = z * ((score * (1 - score)) / self.num_walks) ** 0.5
        else:
            margin = 0.0
            
        ci_low = max(0.0, score - margin)
        ci_high = min(1.0, score + margin)
        
        return ConfidenceResult(
            score=round(score, 4),
            ci_low=round(ci_low, 4),
            ci_high=round(ci_high, 4),
            requires_review=score < self.threshold
        )
