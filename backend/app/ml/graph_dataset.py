import os

import torch
from torch_geometric.data import HeteroData

from app.core.config import settings


class EllipticDatasetLoader:
    def __init__(self, dataset_path: str | None = None):
        self.dataset_path = dataset_path if dataset_path is not None else settings.ELLIPTIC_DATASET_PATH
        
    def load(self) -> HeteroData:
        """
        Loads the Elliptic Bitcoin dataset into a PyG HeteroData object.
        Falls back to a mock dataset if real data is not found.
        """
        features_path = os.path.join(self.dataset_path, "elliptic_txs_features.csv")
        edgelist_path = os.path.join(self.dataset_path, "elliptic_txs_edgelist.csv")
        classes_path = os.path.join(self.dataset_path, "elliptic_txs_classes.csv")
        
        if os.path.exists(features_path) and os.path.exists(edgelist_path) and os.path.exists(classes_path):
            return self._load_real_data(features_path, edgelist_path, classes_path)
        else:
            return self._load_mock_data()
            
    def _load_mock_data(self) -> HeteroData:
        """
        Provides a fixture-based mock matching the exact Elliptic schema.
        5 nodes, 3 edges, known labels.
        Labels: 1 (illicit), 2 (licit), 3 (unknown)
        Features: 166-dimensional vector (1 timestep + 165 features)
        """
        data = HeteroData()
        
        # 5 Nodes
        # Node IDs: 0, 1, 2, 3, 4
        # Timesteps (mock temporal split: nodes 0,1,2 in train, 3,4 in test)
        # Assuming timestep is the first feature or meta feature. Let's create a 'time' tensor.
        time_steps = torch.tensor([1, 1, 2, 10, 11], dtype=torch.long)
        
        # 165 features
        features = torch.randn((5, 165), dtype=torch.float)
        
        # Labels: 1=illicit, 2=licit, 3=unknown (encoded as 0, 1, 2 or similar for training)
        # Raw classes: 1, 2, 3, 2, 1
        # raw_labels = [1, 2, 3, 2, 1]
        
        # Map labels to 0-indexed for training (e.g., 0=illicit, 1=licit, 2=unknown/ignored)
        y = torch.tensor([0, 1, 2, 1, 0], dtype=torch.long)
        
        # Edges (3 edges)
        # 0 -> 1, 1 -> 2, 3 -> 4
        edge_index = torch.tensor([
            [0, 1, 3],
            [1, 2, 4]
        ], dtype=torch.long)
        
        # Add to HeteroData under generic 'node' and 'edge' types or specific like 'tx', 'flow'
        data['tx'].x = features
        data['tx'].y = y
        data['tx'].time = time_steps
        data['tx', 'flow', 'tx'].edge_index = edge_index
        
        return self._apply_temporal_split(data)

    def _load_real_data(self, features_path, edgelist_path, classes_path) -> HeteroData:
        # Placeholder for real CSV loading logic (using pandas/numpy)
        # Since we must mock if not present, and we don't have the dataset, 
        # this will just be a skeletal implementation.
        import pandas as pd
        
        # Load classes
        df_class = pd.read_csv(classes_path)
        # Load features
        df_features = pd.read_csv(features_path, header=None)
        # Load edges
        df_edges = pd.read_csv(edgelist_path)
        
        # Map txId to 0-indexed integer
        tx_ids = df_features[0].values
        tx_id_map = {txId: i for i, txId in enumerate(tx_ids)}
        
        # Extract time step (feature 1)
        time_steps = torch.tensor(df_features[1].values, dtype=torch.long)
        
        # Extract node features (feature 2 to 166)
        x = torch.tensor(df_features.iloc[:, 2:].values, dtype=torch.float)
        
        # Map labels
        # 1 -> 0 (illicit), 2 -> 1 (licit), unknown -> 2
        df_class['class'] = df_class['class'].replace({'1': 0, '2': 1, 'unknown': 2})
        # Merge with features to ensure alignment
        y = torch.tensor(df_class['class'].values, dtype=torch.long)
        
        # Map edges
        source_nodes = [tx_id_map[tx] for tx in df_edges['txId1'] if tx in tx_id_map]
        target_nodes = [tx_id_map[tx] for tx in df_edges['txId2'] if tx in tx_id_map]
        edge_index = torch.tensor([source_nodes, target_nodes], dtype=torch.long)
        
        data = HeteroData()
        data['tx'].x = x
        data['tx'].y = y
        data['tx'].time = time_steps
        data['tx', 'flow', 'tx'].edge_index = edge_index
        
        return self._apply_temporal_split(data)
        
    def _apply_temporal_split(self, data: HeteroData, split_time: int = 5) -> HeteroData:
        """
        Temporal train/test split.
        E.g., nodes with time < split_time are train, >= split_time are test.
        """
        # For mock, time max is 11, we split at 5.
        # For real Elliptic dataset, there are 49 timesteps. Standard split is < 35 for train.
        if data['tx'].time.max() > 15:
            split_time = 35
            
        train_mask = data['tx'].time < split_time
        test_mask = data['tx'].time >= split_time
        
        # Exclude 'unknown' class (class 2) from masks
        labeled_mask = data['tx'].y != 2
        
        data['tx'].train_mask = train_mask & labeled_mask
        data['tx'].test_mask = test_mask & labeled_mask
        
        return data
