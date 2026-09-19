import heapq
import math
from collections import defaultdict

from app.core.config import settings


class DijkstraDecayEngine:
    def __init__(self, decay_lambda: float = settings.DECAY_LAMBDA):
        self.decay_lambda = decay_lambda

    def compute_trace(self, seed_wallet: str, graph_edges_temporal: list[tuple[str, str, float]], vasp_nodes: set[str]) -> tuple:
        """
        Dijkstra with exponential decay weights.
        graph_edges_temporal: (from_node, to_node, timestamp)
        """
        adj = defaultdict(list)
        for u, v, t in graph_edges_temporal:
            adj[u].append((v, t))
            
        # Priority queue stores (cumulative_weight, current_node, current_time, path)
        # Using 0 as initial time doesn't matter for the first hop
        pq = [(0.0, seed_wallet, 0.0, [seed_wallet])]
        
        visited = set()
        
        while pq:
            cost, current, last_time, path = heapq.heappop(pq)
            
            if current in vasp_nodes:
                return path, current
                
            if current in visited:
                continue
            visited.add(current)
            
            for neighbor, t in adj[current]:
                if neighbor not in visited:
                    if last_time == 0.0:
                        # First hop
                        dt = 0
                    else:
                        dt = max(0, t - last_time)
                        
                    weight = math.exp(-self.decay_lambda * dt)
                    # To prefer shorter delays (where weight is closer to 1), we minimize the penalty (1 - weight)
                    penalty = 1.0 - weight
                    heapq.heappush(pq, (cost + penalty, neighbor, t, path + [neighbor]))
                    
        return [], None
