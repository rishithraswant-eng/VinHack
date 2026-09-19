import hashlib
import json
import sys

def verify_merkle(tx_hash, sibling_hashes, is_left_node, merkle_root):
    current = hashlib.sha256(tx_hash.encode("utf-8")).hexdigest()
    for sib_hash, is_left in zip(sibling_hashes, is_left_node):
        if is_left:
            combined = sib_hash + current
        else:
            combined = current + sib_hash
        current = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return current == merkle_root

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_dossier.py <evidence.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()
    except Exception as e:
        print(f"Failed to read file: {e}")
        sys.exit(1)
    
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    print(f"Evidence File SHA-256: {file_hash}")
    
    try:
        data = json.loads(file_bytes.decode("utf-8"))
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        sys.exit(1)
        
    proofs = data.get("merkle_proofs", [])
    if not proofs:
        print("No proofs found in evidence.")
        
    any_fail = False
    for i, p in enumerate(proofs):
        tx_hash = p.get("tx_hash", "")
        root = p.get("merkle_root", "")
        path_hashes = p.get("sibling_hashes", [])
        path_dirs = p.get("is_left_node", [])
        
        verified = verify_merkle(tx_hash, path_hashes, path_dirs, root)
        status = "PASS" if verified else "FAIL"
        print(f"Proof #{i} (tx: {tx_hash}): {status}")
        if not verified:
            any_fail = True
            
    if any_fail:
        print("Verification FAILED.")
        sys.exit(1)
    else:
        print("All proofs verified successfully.")

if __name__ == "__main__":
    main()
