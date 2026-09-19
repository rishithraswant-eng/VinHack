from app.models.canonical import ValidationStatus
from typing import Dict

class FinalityGate:
    def __init__(self, chain_finality_config: Dict[int, int]):
        """
        chain_finality_config: Mapping from chain_id to required confirmation depth.
        """
        self.config = chain_finality_config

    def evaluate(self, chain_id: int, current_confirmations: int) -> ValidationStatus:
        """
        Evaluates whether a transaction meets the finality threshold.
        """
        required_depth = self.config.get(chain_id, 0)
        
        if current_confirmations < required_depth:
            return ValidationStatus.PENDING_FINALITY
            
        return ValidationStatus.UNVERIFIED # Can proceed to cross-validation or other checks
