import torch
import torch.nn as nn
from typing import Tuple
from torch_geometric.nn import RGCNConv, Linear

class RelationalGCN(nn.Module):
    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int, num_relations: int, num_layers: int):
        """
        R-GCN Implementation for multi-relational edge aggregation (Native, ERC20/TRC20, Internal).
        per Schlichtkrull et al.
        """
        super().__init__()
        
        self.num_layers = num_layers
        self.num_relations = num_relations
        
        self.convs = nn.ModuleList()
        # First layer
        self.convs.append(RGCNConv(in_channels, hidden_channels, num_relations))
        
        # Hidden layers
        for _ in range(num_layers - 1):
            self.convs.append(RGCNConv(hidden_channels, hidden_channels, num_relations))
            
        # Classifier
        self.classifier = Linear(hidden_channels, out_channels)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, edge_type: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        x: node features [num_nodes, in_channels]
        edge_index: [2, num_edges]
        edge_type: [num_edges] containing relation type index (0=Native, 1=ERC20/TRC20, 2=Internal)
        
        Returns: (embeddings, logits)
        """
        h = x
        for conv in self.convs:
            h = conv(h, edge_index, edge_type)
            h = torch.relu(h)
            
        logits = self.classifier(h)
        return h, logits
