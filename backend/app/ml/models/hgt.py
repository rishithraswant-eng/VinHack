
import torch
from torch import nn
from torch_geometric.nn import HGTConv, Linear


class HeteroGraphTransformer(nn.Module):
    def __init__(
        self, 
        hidden_channels: int, 
        out_channels: int, 
        num_heads: int, 
        num_layers: int,
        node_types: list[str],
        metadata: tuple[list[str], list[tuple[str, str, str]]]
    ):
        """
        Heterogeneous Graph Transformer (HGT) implementation per Hu et al. WWW 2020.
        Outputs per-node embedding and classification logits.
        """
        super().__init__()
        
        self.node_types = node_types
        self.num_layers = num_layers
        
        # Initial linear projection for each node type to hidden_channels
        self.lin_dict = nn.ModuleDict({
            node_type: Linear(-1, hidden_channels) for node_type in node_types
        })
        
        # HGT layers
        self.convs = nn.ModuleList()
        for _ in range(num_layers):
            conv = HGTConv(hidden_channels, hidden_channels, metadata, num_heads, group='sum')
            self.convs.append(conv)
            
        # Classifier output
        # Classes: mule, mixer, staking, DEX, VASP (5 classes)
        # We output embedding + logits. The linear layer computes logits from embeddings.
        self.classifier = Linear(hidden_channels, out_channels)

    def forward(self, x_dict: dict[str, torch.Tensor], edge_index_dict: dict[tuple[str, str, str], torch.Tensor]) -> dict[str, tuple[torch.Tensor, torch.Tensor]]:
        """
        Forward pass.
        Returns a dict of node_type -> (embedding, logits)
        """
        # 1. Project node features to hidden_channels
        h_dict = {}
        for node_type, x in x_dict.items():
            h_dict[node_type] = self.lin_dict[node_type](x)
            
        # 2. Message passing layers
        for conv in self.convs:
            h_dict = conv(h_dict, edge_index_dict)
            # Add activation and optional dropout
            h_dict = {node_type: torch.relu(h) for node_type, h in h_dict.items()}
            
        # 3. Output embeddings and logits
        output = {}
        for node_type, emb in h_dict.items():
            logits = self.classifier(emb)
            output[node_type] = (emb, logits)
            
        return output
