from abc import ABC, abstractmethod
from typing import Any


class ChainAdapter(ABC):
    @abstractmethod
    def detect_address(self, raw_address: str) -> bool:
        """Validate if raw string is a valid address for this chain."""
        
    @abstractmethod
    def normalize_to_canonical(self, raw_address: str) -> str:
        """Convert a valid address to its canonical representation."""
        
    @abstractmethod
    async def fetch_address_activity(self, address: str, start_time: float | None = None, end_time: float | None = None) -> list[dict[str, Any]]:
        """Fetch transactions associated with an address."""
        
    @abstractmethod
    async def fetch_transaction(self, tx_hash: str) -> dict[str, Any]:
        """Fetch raw transaction payload."""
        
    @abstractmethod
    async def fetch_block_header(self, block_number: int) -> dict[str, Any]:
        """Fetch block header data."""
        
    @abstractmethod
    async def get_finality_depth(self) -> int:
        """Get the current confirmation depth required for finality."""
        
    @abstractmethod
    async def build_inclusion_proof(self, tx_hash: str, block_number: int) -> dict[str, Any]:
        """Build cryptographic proof of inclusion."""
