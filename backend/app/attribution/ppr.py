from collections import defaultdict

from app.core.config import settings


class PPREngine:
    def __init__(self, high_degree_threshold: int = settings.HIGH_DEGREE_THRESHOLD):
        self.high_degree_threshold = high_degree_threshold

    def compute_trace(self, seed_wallet: str, graph_edges: list[tuple], vasp_nodes: set[str], node_degrees: dict[str, int]) -> tuple:
        """
        Bidirectional Personalised PageRank logic.
        seed_wallet: starting node ID
        graph_edges: list of (from_node, to_node)
        vasp_nodes: set of node IDs classified as VASP (absorption states)
        node_degrees: mapping of node ID to its degree (in + out)
        """
        # Adjacency list
        adj = defaultdict(list)
        for u, v in graph_edges:
            adj[u].append(v)
            
        visited = set()
        queue = [(seed_wallet, [seed_wallet])]
        
        while queue:
            current, path = queue.pop(0)
            
            if current in vasp_nodes:
                return path, current
                
            # High-degree guard
            if node_degrees.get(current, 0) > self.high_degree_threshold:
                continue
                
            visited.add(current)
            for neighbor in adj[current]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
                    
        return [], None
