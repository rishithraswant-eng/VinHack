import hashlib
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.audit.verifier import AuditVerifier
from app.models.canonical import AuditLog


@pytest.mark.asyncio
async def test_audit_chain_valid():
    session = AsyncMock()
    
    # Construct a valid chain
    digest1 = b"payload1"
    hash1 = hashlib.sha256(digest1).digest()
    log1 = AuditLog(id=1, prev_entry_hash=None, payload_digest=digest1, entry_hash=hash1)
    
    digest2 = b"payload2"
    hash2 = hashlib.sha256(hash1 + digest2).digest()
    log2 = AuditLog(id=2, prev_entry_hash=hash1, payload_digest=digest2, entry_hash=hash2)
    
    # Mock session.execute().scalars().all()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [log1, log2]
    session.execute.return_value = mock_result
    
    is_valid, errors = await AuditVerifier.verify_audit_chain(session)
    assert is_valid is True
    assert len(errors) == 0

@pytest.mark.asyncio
async def test_audit_chain_invalid_hash():
    session = AsyncMock()
    
    digest1 = b"payload1"
    hash1 = hashlib.sha256(digest1).digest()
    log1 = AuditLog(id=1, prev_entry_hash=None, payload_digest=digest1, entry_hash=hash1)
    
    digest2 = b"payload2"
    # Provide a tampered hash
    hash2_tampered = hashlib.sha256(b"tampered").digest()
    log2 = AuditLog(id=2, prev_entry_hash=hash1, payload_digest=digest2, entry_hash=hash2_tampered)
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [log1, log2]
    session.execute.return_value = mock_result
    
    is_valid, errors = await AuditVerifier.verify_audit_chain(session)
    assert is_valid is False
    assert len(errors) == 1
    assert errors[0]['error'] == "HASH_MISMATCH"

@pytest.mark.asyncio
async def test_audit_chain_row_deletion():
    session = AsyncMock()
    
    digest1 = b"payload1"
    hash1 = hashlib.sha256(digest1).digest()
    log1 = AuditLog(id=1, prev_entry_hash=None, payload_digest=digest1, entry_hash=hash1)
    
    # Skip ID 2
    digest3 = b"payload3"
    hash3 = hashlib.sha256(hash1 + digest3).digest() # assumes deleted row didn't exist for hash logic
    log3 = AuditLog(id=3, prev_entry_hash=hash1, payload_digest=digest3, entry_hash=hash3)
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [log1, log3]
    session.execute.return_value = mock_result
    
    is_valid, errors = await AuditVerifier.verify_audit_chain(session)
    assert is_valid is False
    assert any(e['error'] == "ROW_DELETION_DETECTED" for e in errors)
