"""
Unit tests for structured logging and correlation-id propagation (ES-05).
"""

import json
import logging

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.logging import (
    CORRELATION_ID_HEADER,
    JSONFormatter,
    correlation_id_ctx,
)
from app.main import app


def test_json_formatter_outputs_expected_fields():
    """Verify JSONFormatter includes all mandatory forensic tracking fields."""
    formatter = JSONFormatter(service_name="test-service")
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_file.py",
        lineno=42,
        msg="Test message for structured logging",
        args=(),
        exc_info=None,
    )

    token = correlation_id_ctx.set("corr-test-12345")
    try:
        formatted = formatter.format(record)
        log_json = json.loads(formatted)

        assert log_json["level"] == "INFO"
        assert log_json["service"] == "test-service"
        assert log_json["correlation_id"] == "corr-test-12345"
        assert log_json["message"] == "Test message for structured logging"
        assert log_json["file"] == "test_file.py"
        assert log_json["line"] == 42
        assert "timestamp" in log_json
    finally:
        correlation_id_ctx.reset(token)


@pytest.mark.asyncio
async def test_correlation_id_generated_when_missing():
    """Verify that incoming requests without X-Correlation-ID receive a generated ID."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert CORRELATION_ID_HEADER in response.headers
        corr_id = response.headers[CORRELATION_ID_HEADER]
        assert corr_id.startswith("ph-")
        assert "X-Response-Time-Ms" in response.headers


@pytest.mark.asyncio
async def test_correlation_id_propagated_when_provided():
    """Verify that incoming X-Correlation-ID is preserved and echoed in response."""
    custom_id = "lea-case-fir-998822"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get(
            "/health",
            headers={CORRELATION_ID_HEADER: custom_id},
        )
        assert response.status_code == 200
        assert response.headers[CORRELATION_ID_HEADER] == custom_id
