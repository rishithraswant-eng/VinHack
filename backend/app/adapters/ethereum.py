from typing import Dict, Any, List, Optional
from decimal import Decimal
from eth_utils import is_address, to_checksum_address
from backend.app.adapters.base import ChainAdapter

class EthereumAdapter(ChainAdapter):
    def detect_address(self, raw_address: str) -> bool:
        if not raw_address:
            return False
        # is_address checks if it's a valid hex address, optionally checking EIP-55 if mixed case
        return is_address(raw_address)
        
    def normalize_to_canonical(self, raw_address: str) -> str:
        if not self.detect_address(raw_address):
            raise ValueError(f"Invalid Ethereum address: {raw_address}")
        # EIP-55 checksum format is the canonical representation
        return to_checksum_address(raw_address)
        
    async def fetch_address_activity(self, address: str, start_time: Optional[float] = None, end_time: Optional[float] = None) -> List[Dict[str, Any]]:
        # Mock implementation
        return []
        
    async def fetch_transaction(self, tx_hash: str) -> Dict[str, Any]:
        # Mock implementation
        return {}
        
    async def fetch_block_header(self, block_number: int) -> Dict[str, Any]:
        # Mock implementation
        return {}
        
    async def get_finality_depth(self) -> int:
        return 64 # ~12 minutes on ETH PoS (roughly 2 epochs)
        
    async def build_inclusion_proof(self, tx_hash: str, block_number: int) -> Dict[str, Any]:
        # Mock implementation
        return {"proof_kind": "ETH_MPT_TRANSACTION"}
        
    # Ethereum-specific methods
    def decode_transfer_events(self, receipt_logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Decodes ERC-20 Transfer events from transaction receipt logs.
        Transfer topic: 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
        """
        TRANSFER_EVENT_TOPIC = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
        transfers = []
        for log in receipt_logs:
            topics = log.get('topics', [])
            if not topics or topics[0] != TRANSFER_EVENT_TOPIC:
                continue
                
            if len(topics) == 3: # ERC-20 Transfer
                # Topics 1 and 2 are from and to addresses (padded to 32 bytes)
                from_addr = "0x" + topics[1][-40:]
                to_addr = "0x" + topics[2][-40:]
                
                try:
                    from_addr = to_checksum_address(from_addr)
                    to_addr = to_checksum_address(to_addr)
                except ValueError:
                    continue
                    
                # Data contains the value
                data = log.get('data', '0x')
                if data == '0x':
                    value = Decimal(0)
                else:
                    try:
                        value = Decimal(int(data, 16))
                    except ValueError:
                        value = Decimal(0)
                        
                transfers.append({
                    "contract_address": to_checksum_address(log.get('address', '')),
                    "from_address": from_addr,
                    "to_address": to_addr,
                    "value_base": value
                })
        return transfers
        
    def analyze_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes a transaction for nonce sequencing and contract creation.
        """
        is_contract_creation = False
        to_address = tx.get("to")
        
        # In Ethereum, a transaction with no 'to' address is a contract creation
        if not to_address or to_address == '0x' or to_address == '0x0':
            is_contract_creation = True
            
        return {
            "nonce": tx.get("nonce", 0),
            "is_contract_creation": is_contract_creation,
            "value_base": Decimal(tx.get("value", 0))
        }
