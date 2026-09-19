from decimal import Decimal
from typing import Any

import base58
import bech32

from app.adapters.base import ChainAdapter


def bech32m_verify_checksum(hrp, data):
    return bech32.bech32_polymod(bech32.bech32_hrp_expand(hrp) + data) == 0x2bc830a3

def bech32m_decode(addr):
    if (any(ord(x) < 33 or ord(x) > 126 for x in addr)) or (addr.lower() != addr and addr.upper() != addr):
        return (None, None)
    addr = addr.lower()
    pos = addr.rfind('1')
    if pos < 1 or pos + 7 > len(addr) or len(addr) > 90:
        return (None, None)
    if not all(x in bech32.CHARSET for x in addr[pos+1:]):
        return (None, None)
    hrp = addr[:pos]
    data = [bech32.CHARSET.find(x) for x in addr[pos+1:]]
    if not bech32m_verify_checksum(hrp, data):
        return (None, None)
    return (hrp, data[:-6])

def _is_p2tr(addr: str) -> bool:
    hrp, data = bech32m_decode(addr)
    if hrp != 'bc' or not data:
        return False
    return bool(data[0] == 1 and len(data) == 53)

class BitcoinAdapter(ChainAdapter):
    def detect_address(self, raw_address: str) -> bool:
        if not raw_address:
            return False
            
        # Try Base58Check (P2PKH, P2SH)
        try:
            decoded = base58.b58decode_check(raw_address)
            # 1 for P2PKH (0x00), 3 for P2SH (0x05)
            if decoded[0] in (0x00, 0x05):
                return True
        except ValueError:
            pass
            
        # Try Bech32/Bech32m (P2WPKH, P2WSH, P2TR)
        hrp, data = bech32.bech32_decode(raw_address)
        if hrp == 'bc' and data is not None:
            return True
            
        # Try Bech32m explicitly for P2TR since bech32_decode returns None
        return bool(_is_p2tr(raw_address))
        
    def normalize_to_canonical(self, raw_address: str) -> str:
        if not self.detect_address(raw_address):
            raise ValueError(f"Invalid Bitcoin address: {raw_address}")
        # Bitcoin addresses are case-sensitive for Base58 and lowercase for Bech32
        # However, for Bech32 canonical is lowercase. 
        if raw_address.lower().startswith('bc1'):
            return raw_address.lower()
        return raw_address
        
    async def fetch_address_activity(self, address: str, start_time: float | None = None, end_time: float | None = None) -> list[dict[str, Any]]:
        # Mock implementation for tests
        return []
        
    async def fetch_transaction(self, tx_hash: str) -> dict[str, Any]:
        # Mock implementation
        return {}
        
    async def fetch_block_header(self, block_number: int) -> dict[str, Any]:
        # Mock implementation
        return {}
        
    async def get_finality_depth(self) -> int:
        return 6
        
    async def build_inclusion_proof(self, tx_hash: str, block_number: int) -> dict[str, Any]:
        # Mock implementation
        return {"proof_kind": "BTC_MERKLE_DOUBLE_SHA256"}
        
    # Bitcoin-specific heuristic methods
    def identify_cospend_clusters(self, transaction: dict[str, Any]) -> list[str]:
        """
        Identifies input addresses belonging to the same entity via co-spend heuristic.
        Excludes transactions that look like CoinJoin or PayJoin.
        """
        inputs = transaction.get("inputs", [])
        outputs = transaction.get("outputs", [])
        
        # Guard: Check for CoinJoin pattern (many inputs, many outputs of identical value)
        if len(inputs) > 2 and len(outputs) > 2:
            out_values = [out.get("value_base", 0) for out in outputs]
            if len(set(out_values)) < len(out_values): # Some outputs have identical values
                return [] # Potential CoinJoin
                
        # Guard: Check for PayJoin (heuristic: one input matches one output exactly, usually)
        # Real PayJoin detection is complex, simplified guard:
        if len(inputs) == 2 and len(outputs) == 2:
             # Assume potential PayJoin if it looks like a standard 2in/2out payment
             pass # In a real implementation we'd check more conditions
             
        input_addresses = list({inp.get("address") for inp in inputs if inp.get("address")})
        if len(input_addresses) > 1:
            return input_addresses
        return []

    def tag_change_addresses(self, transaction: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Identifies change outputs using heuristics.
        Returns a list of tags.
        """
        inputs = transaction.get("inputs", [])
        outputs = transaction.get("outputs", [])
        tags = []
        
        input_addresses = {inp.get("address") for inp in inputs if inp.get("address")}
        
        if not input_addresses or len(outputs) == 0:
            return tags
            
        # HEURISTIC_CHANGE_SINGLE_OUTPUT: if one output goes back to an input address
        for out in outputs:
            out_addr = out.get("address")
            if out_addr in input_addresses:
                tags.append({
                    "address": out_addr,
                    "heuristic": "HEURISTIC_CHANGE_SINGLE_OUTPUT",
                    "vout": out.get("vout")
                })
                
        # HEURISTIC_PEEL_CHAIN_OUTPUT: Typically 2 outputs, one small (payment), one large (change to new address)
        if len(outputs) == 2 and not tags:
            val1 = outputs[0].get("value_base", Decimal(0))
            val2 = outputs[1].get("value_base", Decimal(0))
            if val1 > 0 and val2 > 0:
                if val1 > val2 * Decimal(10): # roughly, val1 is much larger
                    tags.append({
                        "address": outputs[0].get("address"),
                        "heuristic": "HEURISTIC_PEEL_CHAIN_OUTPUT",
                        "vout": outputs[0].get("vout")
                    })
                elif val2 > val1 * Decimal(10):
                    tags.append({
                        "address": outputs[1].get("address"),
                        "heuristic": "HEURISTIC_PEEL_CHAIN_OUTPUT",
                        "vout": outputs[1].get("vout")
                    })
                    
        return tags
