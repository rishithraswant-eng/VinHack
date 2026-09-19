from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from decimal import Decimal

class ChainAdapter(ABC):
    @abstractmethod
    def detect_address(self, raw_address: str) -> bool:
        """Validate if raw string is a valid address for this chain."""
        pass
        
    @abstractmethod
    def normalize_to_canonical(self, raw_address: str) -> str:
        """Convert a valid address to its canonical representation."""
        pass
        
    @abstractmethod
    async def fetch_address_activity(self, address: str, start_time: Optional[float] = None, end_time: Optional[float] = None) -> List[Dict[str, Any]]:
        """Fetch transactions associated with an address."""
        pass
        
    @abstractmethod
    async def fetch_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Fetch raw transaction payload."""
        pass
        
    @abstractmethod
    async def fetch_block_header(self, block_number: int) -> Dict[str, Any]:
        """Fetch block header data."""
        pass
        
    @abstractmethod
    async def get_finality_depth(self) -> int:
        """Get the current confirmation depth required for finality."""
        pass
        
    @abstractmethod
    async def build_inclusion_proof(self, tx_hash: str, block_number: int) -> Dict[str, Any]:
        """Build cryptographic proof of inclusion."""
        pass
