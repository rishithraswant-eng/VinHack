"""
PHANTASM Core API Application.
Entry point for the FastAPI application server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import cases, trace
from app.core.config import settings
from app.core.logging import CorrelationIdMiddleware, setup_logging

# Initialize structured logging
setup_logging(log_level=settings.LOG_LEVEL, service_name="phantasm-api")

app = FastAPI(
    title="PHANTASM — Forensic Attribution Engine",
    description=(
        "Probabilistic Heterogeneous Attribution & Nexus Trace for Automated SAHYOG Mapping. "
        "Built for Indian Law Enforcement Agencies (MHA / I4C) under SIH26182."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Attach Correlation ID middleware first (ES-05)
app.add_middleware(CorrelationIdMiddleware)

# Attach CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(cases.router, prefix=settings.API_V1_STR, tags=["cases"])
app.include_router(trace.router, prefix=settings.API_V1_STR, tags=["traces"])


@app.get("/health", tags=["System"])
@app.get(f"{settings.API_V1_STR}/health", tags=["System"])
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": "phantasm-core-api",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "sahyog_mode": settings.SAHYOG_CONNECTOR_MODE,
    }
