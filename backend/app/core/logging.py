"""
Structured logging and correlation-id management.
Implements Engineering Standard ES-05:
Structured logging with a correlation id propagated across every service hop.
"""

import json
import logging
import time
import uuid
from collections.abc import Callable
from contextvars import ContextVar
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Context variable to hold the correlation ID for the current request context
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="")

CORRELATION_ID_HEADER = "X-Correlation-ID"


def get_correlation_id() -> str:
    """Retrieve the current correlation ID, or return empty string if outside request."""
    return correlation_id_ctx.get()


class JSONFormatter(logging.Formatter):
    """
    JSON log formatter emitting structured JSON for each log record.
    Includes timestamp, level, correlation_id, service name, message, and caller info.
    """

    def __init__(self, service_name: str = "phantasm-core"):
        super().__init__()
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "service": self.service_name,
            "correlation_id": get_correlation_id(),
            "logger": record.name,
            "message": record.getMessage(),
            "file": record.filename,
            "line": record.lineno,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Include any extra attributes attached to the LogRecord
        if hasattr(record, "extra_fields") and isinstance(record.extra_fields, dict):
            log_data.update(record.extra_fields)

        return json.dumps(log_data)


def setup_logging(log_level: str = "INFO", service_name: str = "phantasm-core") -> None:
    """Configure root logger with structured JSON formatting."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Remove existing handlers to avoid duplicates
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(JSONFormatter(service_name=service_name))
    root_logger.addHandler(stream_handler)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    FastAPI / Starlette Middleware that extracts or generates an X-Correlation-ID
    for every HTTP request, stores it in ContextVar for logging, and returns
    it in the response headers.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        corr_id = request.headers.get(CORRELATION_ID_HEADER)
        if not corr_id:
            corr_id = f"ph-{uuid.uuid4().hex[:16]}"

        token = correlation_id_ctx.set(corr_id)
        start_time = time.perf_counter()

        logger = logging.getLogger("phantasm.access")
        logger.info(
            f"Incoming request {request.method} {request.url.path}",
            extra={"extra_fields": {"method": request.method, "path": request.url.path}},
        )

        try:
            response: Response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            response.headers[CORRELATION_ID_HEADER] = corr_id
            response.headers["X-Response-Time-Ms"] = str(duration_ms)

            logger.info(
                f"Completed request {request.method} {request.url.path} with status {response.status_code} in {duration_ms}ms",
                extra={
                    "extra_fields": {
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                    }
                },
            )
            return response
        finally:
            correlation_id_ctx.reset(token)
