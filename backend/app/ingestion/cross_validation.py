import hashlib
import json
from typing import Any

from app.core.ratelimit import AsyncTokenBucket, with_exponential_backoff
from app.models.canonical import ValidationStatus


class CrossValidator:
    def __init__(self, token_bucket: AsyncTokenBucket = None):
        self.bucket = token_bucket or AsyncTokenBucket(capacity=100.0, fill_rate=10.0)

    @staticmethod
    def compute_canonical_digest(
        chain_id: int, 
        block_number: int, 
        tx_hash: str, 
        from_address: str, 
        to_address: str, 
        amount: str, 
        asset_id: str
    ) -> bytes:
        payload = {
            "chain_id": chain_id,
            "block_number": block_number,
            "tx_hash": tx_hash,
            "from": from_address,
            "to": to_address,
            "amount": amount,
            "asset_id": asset_id
        }
        encoded = json.dumps(payload, sort_keys=True).encode('utf-8')
        return hashlib.sha256(encoded).digest()

    @with_exponential_backoff(max_retries=3)
    async def fetch_from_provider(self, provider_mock_func, *args, **kwargs) -> dict[str, Any]:
        """Wrapper to fetch data with rate limiting and backoff."""
        await self.bucket.consume(1.0)
        return await provider_mock_func(*args, **kwargs)

    def validate_responses(self, responses: list[dict[str, Any]]) -> tuple[ValidationStatus, dict[str, Any] | None]:
        if not responses:
            return ValidationStatus.UNVERIFIED, None
        
        if len(responses) == 1:
            return ValidationStatus.SINGLE_SOURCE, None
            
        # Ensure all responses match exactly on the canonical digest
        first_digest = responses[0].get("canonical_digest")
        first_data = responses[0].get("data", {})
        
        diffs = {}
        is_conflicted = False
        
        for idx, resp in enumerate(responses[1:], start=1):
            if resp.get("canonical_digest") != first_digest:
                is_conflicted = True
                curr_data = resp.get("data", {})
                
                # Compute field-level diff between first_data and curr_data
                all_keys = set(first_data.keys()).union(curr_data.keys())
                for key in all_keys:
                    val1 = first_data.get(key)
                    val2 = curr_data.get(key)
                    if val1 != val2:
                        diff_key = f"provider_0_vs_{idx}_{key}"
                        diffs[diff_key] = {"expected": val1, "actual": val2}
                        
        if is_conflicted:
            return ValidationStatus.CONFLICTED, diffs
            
        return ValidationStatus.CROSS_VALIDATED, None
