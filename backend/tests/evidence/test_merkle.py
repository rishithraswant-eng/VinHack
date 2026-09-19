import pytest
from app.evidence.merkle import MerkleEngine, MerkleProof

def test_merkle_proof_verification():
    txs = ["tx1", "tx2", "tx3", "tx4"]
    proof = MerkleEngine.build_proof("tx2", txs)
    
    # Valid proof should verify
    assert MerkleEngine.verify_proof(proof) is True
    
    # Tampered tx hash should fail
    tampered_proof = MerkleProof(
        tx_hash="tx_tampered",
        sibling_hashes=proof.sibling_hashes,
        is_left_node=proof.is_left_node,
        merkle_root=proof.merkle_root
    )
    assert MerkleEngine.verify_proof(tampered_proof) is False
