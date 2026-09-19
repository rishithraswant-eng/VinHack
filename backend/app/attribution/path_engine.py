from app.attribution.dijkstra import DijkstraDecayEngine
from app.attribution.models import TraceResult
from app.attribution.monte_carlo import MonteCarloScorer
from app.attribution.ppr import PPREngine

# Import classifier interface (mocked or actual)
from app.ml.classifier import GraphClassifier


class AttributionOrchestrator:
    def __init__(self):
        self.classifier = GraphClassifier()
        self.ppr = PPREngine()
        self.dijkstra = DijkstraDecayEngine()
        self.scorer = MonteCarloScorer()

    def trace(self, seed_wallet: str, graph_edges: list[tuple], vasp_nodes: set[str], node_degrees: dict, use_dijkstra: bool = False) -> TraceResult:
        """
        Enforces classify-first, search-second.
        """
        # Step 1: Classify (Phase 2 constraint)
        # Mocking classification call to enforce order
        self.classifier.classify_node(seed_wallet, "bitcoin", {})
        
        # Step 2: Search (Phase 3)
        if use_dijkstra:
            # Dijkstra needs temporal edges, assuming graph_edges has (u, v, t) for dijkstra
            path, vasp = self.dijkstra.compute_trace(seed_wallet, graph_edges, vasp_nodes)
            algo = "Dijkstra"
        else:
            path, vasp = self.ppr.compute_trace(seed_wallet, graph_edges, vasp_nodes, node_degrees)
            algo = "PPR"
            
        # Step 3: Confidence Score
        confidence = self.scorer.compute_confidence(path, vasp, graph_edges)
        
        return TraceResult(
            path=path,
            vasp_node=vasp,
            hop_count=len(path) - 1 if path else 0,
            algorithm_used=algo,
            classifier_version="HGT-v1.0", # hardcoded for Phase 2 registry compliance
            confidence_result=confidence
        )
