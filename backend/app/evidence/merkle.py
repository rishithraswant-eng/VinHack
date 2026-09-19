import hashlib
import json
from typing import List, Dict, Any
from pydantic import BaseModel

class MerkleProof(BaseModel):
    tx_hash: str
    sibling_hashes: List[str]
    is_left_node: List[bool]
    merkle_root: str

    def to_json(self) -> str:
        return json.dumps(self.dict())

class MerkleEngine:
    @staticmethod
    def _hash(data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @classmethod
    def build_proof(cls, tx_hash: str, block_txs: List[str]) -> MerkleProof:
        """
        Constructs O(log N) sibling-hash path.
        """
        if tx_hash not in block_txs:
            raise ValueError("tx_hash not in block_txs")
            
        # Ensure even number of leaves
        leaves = [cls._hash(tx) for tx in block_txs]
        target_hash = cls._hash(tx_hash)
        
        target_idx = leaves.index(target_hash)
        
        sibling_hashes = []
        is_left_node = []
        
        current_layer = leaves
        idx = target_idx
        
        while len(current_layer) > 1:
            if len(current_layer) % 2 != 0:
                current_layer.append(current_layer[-1])
                
            next_layer = []
            for i in range(0, len(current_layer), 2):
                h1 = current_layer[i]
                h2 = current_layer[i+1]
                next_layer.append(cls._hash(h1 + h2))
                
                if i == idx or i + 1 == idx:
                    if i == idx:
                        sibling_hashes.append(h2)
                        is_left_node.append(False)
                    else:
                        sibling_hashes.append(h1)
                        is_left_node.append(True)
                        
            current_layer = next_layer
            idx = idx // 2
            
        return MerkleProof(
            tx_hash=tx_hash,
            sibling_hashes=sibling_hashes,
            is_left_node=is_left_node,
            merkle_root=current_layer[0]
        )
        
    @classmethod
    def verify_proof(cls, proof: MerkleProof) -> bool:
        """
        Standalone verification function.
        """
        current_hash = cls._hash(proof.tx_hash)
        
        for sibling, is_left in zip(proof.sibling_hashes, proof.is_left_node):
            if is_left:
                current_hash = cls._hash(sibling + current_hash)
            else:
                current_hash = cls._hash(current_hash + sibling)
                
        return current_hash == proof.merkle_root

# Expose at module level for smoke testing
def build_proof(tx_hash: str, block_txs: List[str]) -> MerkleProof:
    return MerkleEngine.build_proof(tx_hash, block_txs)

def verify_proof(proof: MerkleProof) -> bool:
    return MerkleEngine.verify_proof(proof)
