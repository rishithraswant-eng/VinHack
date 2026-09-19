import hashlib
import json
from typing import List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.canonical import AuditLog

class AuditVerificationException(Exception):
    pass

class AuditVerifier:
    @staticmethod
    def _compute_hash(prev_hash: bytes, payload_digest: bytes) -> bytes:
        hasher = hashlib.sha256()
        if prev_hash:
            hasher.update(prev_hash)
        if payload_digest:
            hasher.update(payload_digest)
        return hasher.digest()

    @staticmethod
    async def verify_audit_chain(session: AsyncSession, start_id: int = None, end_id: int = None) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Verifies the integrity of the audit chain by recomputing hashes.
        Returns a tuple of (is_valid, list_of_errors).
        """
        query = select(AuditLog).order_by(AuditLog.id.asc())
        
        if start_id is not None:
            query = query.filter(AuditLog.id >= start_id)
        if end_id is not None:
            query = query.filter(AuditLog.id <= end_id)

        result = await session.execute(query)
        logs: List[AuditLog] = result.scalars().all()

        errors = []
        expected_prev_hash = None

        # Fetch the very first log prior to start_id if needed to establish expected_prev_hash
        if start_id is not None and len(logs) > 0:
            if logs[0].prev_entry_hash:
                expected_prev_hash = logs[0].prev_entry_hash

        for log in logs:
            if expected_prev_hash is not None and log.prev_entry_hash != expected_prev_hash:
                errors.append({
                    "id": log.id,
                    "error": "CHAIN_BROKEN_PREV_HASH_MISMATCH",
                    "expected": expected_prev_hash.hex() if expected_prev_hash else None,
                    "actual": log.prev_entry_hash.hex() if log.prev_entry_hash else None
                })
            
            recomputed_hash = AuditVerifier._compute_hash(log.prev_entry_hash, log.payload_digest)
            
            if recomputed_hash != log.entry_hash:
                errors.append({
                    "id": log.id,
                    "error": "HASH_MISMATCH",
                    "expected": recomputed_hash.hex(),
                    "actual": log.entry_hash.hex() if log.entry_hash else None
                })

            expected_prev_hash = log.entry_hash

        # Also detect if any IDs were skipped (deletion)
        if logs:
            first_id = logs[0].id
            last_id = logs[-1].id
            if len(logs) != (last_id - first_id + 1):
                errors.append({
                    "error": "ROW_DELETION_DETECTED",
                    "details": f"Expected {last_id - first_id + 1} rows, found {len(logs)}"
                })

        return len(errors) == 0, errors
