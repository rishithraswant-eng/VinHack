"""
Application Configuration.
Strictly maps system settings, database URLs, RPC keys, and finality depths.
"""


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True
    SECRET_KEY: str = "phantasm_super_secure_secret_key_change_in_production_32_chars_min"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PHANTASM — Forensic Attribution Engine"

    # PostgreSQL / Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "phantasm"
    POSTGRES_PASSWORD: str = "phantasm_dev_secret"
    POSTGRES_DB: str = "phantasm"
    DATABASE_URL: str = (
        "postgresql+psycopg://phantasm:phantasm_dev_secret@localhost:5432/phantasm"
    )
    FALLBACK_SQLITE_URL: str = "sqlite:///./phantasm_dev.db"

    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "phantasm_dev_secret"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # MinIO / S3
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "phantasm_minio"
    MINIO_SECRET_KEY: str = "phantasm_minio_secret"
    MINIO_BUCKET_DOSSIERS: str = "phantasm-dossiers"
    MINIO_BUCKET_MODELS: str = "phantasm-models"
    MINIO_BUCKET_EVIDENCE: str = "phantasm-evidence"
    MINIO_SECURE: bool = False

    # External APIs
    ETHERSCAN_API_KEY: str = ""
    ALCHEMY_API_KEY: str = ""
    BLOCKCHAIR_API_KEY: str = ""
    MEMPOOL_SPACE_API_URL: str = "https://mempool.space/api"
    BITQUERY_API_KEY: str = ""

    # Finality confirmation depths (PRD C1, T1.ING.07)
    FINALITY_CONFIRMATIONS_BITCOIN: int = 6
    FINALITY_CONFIRMATIONS_ETHEREUM: int = 12
    FINALITY_CONFIRMATIONS_TRON: int = 19
    FINALITY_CONFIRMATIONS_SOLANA: int = 32

    # SAHYOG Interface
    SAHYOG_CONNECTOR_MODE: str = "MOCK"
    SAHYOG_API_URL: str = "https://mock.sahyog.internal/api/v2"
    SAHYOG_API_KEY: str = "mock_sahyog_dev_token"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # ML & Intelligence Core
    ELLIPTIC_DATASET_PATH: str = "./data/elliptic"
    HAWKES_MU: float = 0.1
    HAWKES_ALPHA: float = 0.5
    HAWKES_BETA: float = 1.0

    # Phase 3 Attribution Configuration
    HIGH_DEGREE_THRESHOLD: int = 10000
    DECAY_LAMBDA: float = 0.01
    RWR_WALKS: int = 1000
    CONFIDENCE_THRESHOLD: float = 0.75


settings = Settings()
