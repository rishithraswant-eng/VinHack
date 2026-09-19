
import enum
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, 
    Text, SmallInteger, BigInteger, LargeBinary, CheckConstraint, 
    UniqueConstraint, Index, func, Float, Date, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
from sqlalchemy.ext.declarative import declarative_base

from app.models.base import Base

# ==========================================
# ENUMS
# ==========================================
class ChainModel(str, enum.Enum):
    UTXO = 'UTXO'
    ACCOUNT = 'ACCOUNT'

class CaseStatus(str, enum.Enum):
    DRAFT = 'DRAFT'
    ACTIVE = 'ACTIVE'
    REVIEW_REQUIRED = 'REVIEW_REQUIRED'
    ATTRIBUTED = 'ATTRIBUTED'
    DISPATCHED = 'DISPATCHED'
    RESPONDED = 'RESPONDED'
    SUSPENDED = 'SUSPENDED'
    CLOSED = 'CLOSED'
    ARCHIVED = 'ARCHIVED'

class CaseType(str, enum.Enum):
    INVESTMENT_FRAUD = 'INVESTMENT_FRAUD'
    RANSOMWARE = 'RANSOMWARE'
    SEXTORTION = 'SEXTORTION'
    PHISHING = 'PHISHING'
    MULE_NETWORK = 'MULE_NETWORK'
    DRUG_TRAFFICKING = 'DRUG_TRAFFICKING'
    TERROR_FINANCE = 'TERROR_FINANCE'
    EXCHANGE_HACK = 'EXCHANGE_HACK'
    PIG_BUTCHERING = 'PIG_BUTCHERING'
    OTHER = 'OTHER'

class TraceStatus(str, enum.Enum):
    QUEUED = 'QUEUED'
    INGESTING = 'INGESTING'
    PRUNING = 'PRUNING'
    CLASSIFYING = 'CLASSIFYING'
    SEARCHING = 'SEARCHING'
    SCORING = 'SCORING'
    SEALING = 'SEALING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'
    BUDGET_EXCEEDED = 'BUDGET_EXCEEDED'
    NO_PATH_FOUND = 'NO_PATH_FOUND'
    TERMINATED_AT_OBFUSCATOR = 'TERMINATED_AT_OBFUSCATOR'

class NodeClass(str, enum.Enum):
    EOA_PERSONAL = 'EOA_PERSONAL'
    MULE = 'MULE'
    VASP_DEPOSIT = 'VASP_DEPOSIT'
    VASP_HOT = 'VASP_HOT'
    VASP_COLD = 'VASP_COLD'
    MIXER = 'MIXER'
    BRIDGE = 'BRIDGE'
    DEX_ROUTER = 'DEX_ROUTER'
    DEX_POOL = 'DEX_POOL'
    STAKING = 'STAKING'
    CONTRACT_OTHER = 'CONTRACT_OTHER'
    MERCHANT_PSP = 'MERCHANT_PSP'
    GAMBLING = 'GAMBLING'
    MINER = 'MINER'
    SANCTIONED = 'SANCTIONED'
    UNKNOWN = 'UNKNOWN'

class TemporalPattern(str, enum.Enum):
    ORGANIC = 'ORGANIC'
    PEEL_CHAIN = 'PEEL_CHAIN'
    SMURFING = 'SMURFING'
    BOT_BURST = 'BOT_BURST'
    DUST_STORM = 'DUST_STORM'
    INSUFFICIENT_DATA = 'INSUFFICIENT_DATA'

class ValidationStatus(str, enum.Enum):
    CROSS_VALIDATED = 'CROSS_VALIDATED'
    SINGLE_SOURCE = 'SINGLE_SOURCE'
    CONFLICTED = 'CONFLICTED'
    PENDING_FINALITY = 'PENDING_FINALITY'
    REORGED = 'REORGED'
    UNVERIFIED = 'UNVERIFIED'

class ProofStatus(str, enum.Enum):
    VERIFIED = 'VERIFIED'
    FAILED = 'FAILED'
    UNAVAILABLE = 'UNAVAILABLE'
    NOT_APPLICABLE = 'NOT_APPLICABLE'
    PENDING = 'PENDING'

class ProofKind(str, enum.Enum):
    BTC_MERKLE_DOUBLE_SHA256 = 'BTC_MERKLE_DOUBLE_SHA256'
    ETH_MPT_RECEIPT = 'ETH_MPT_RECEIPT'
    ETH_MPT_TRANSACTION = 'ETH_MPT_TRANSACTION'
    TRON_TX_MERKLE = 'TRON_TX_MERKLE'
    SOLANA_ENTRY_ATTESTATION = 'SOLANA_ENTRY_ATTESTATION'
    HEADER_ANCHORED_DIGEST = 'HEADER_ANCHORED_DIGEST'

class Jurisdiction(str, enum.Enum):
    FIU_REGISTERED_DOMESTIC = 'FIU_REGISTERED_DOMESTIC'
    FIU_REGISTERED_OFFSHORE = 'FIU_REGISTERED_OFFSHORE'
    NOT_REGISTERED_OFFSHORE = 'NOT_REGISTERED_OFFSHORE'
    UNKNOWN_ENTITY = 'UNKNOWN_ENTITY'
    SANCTIONED_JURISDICTION = 'SANCTIONED_JURISDICTION'

class DisclosureStatus(str, enum.Enum):
    DRAFT = 'DRAFT'
    PENDING_APPROVAL = 'PENDING_APPROVAL'
    SIGNED = 'SIGNED'
    SUBMITTED = 'SUBMITTED'
    ACKNOWLEDGED = 'ACKNOWLEDGED'
    RESPONDED = 'RESPONDED'
    REJECTED = 'REJECTED'
    WITHDRAWN = 'WITHDRAWN'
    ERRATUM_ISSUED = 'ERRATUM_ISSUED'
    CLOSED = 'CLOSED'

class LegalBasis(str, enum.Enum):
    SEC_94_BNSS_2023 = 'SEC_94_BNSS_2023'
    SEC_79_3_B_IT_ACT_2000 = 'SEC_79_3_B_IT_ACT_2000'
    SEC_91_CRPC_LEGACY = 'SEC_91_CRPC_LEGACY'
    MLAT_REQUEST = 'MLAT_REQUEST'
    INTERPOL_CHANNEL = 'INTERPOL_CHANNEL'
    PRESERVATION_ORDER = 'PRESERVATION_ORDER'

class ModelStage(str, enum.Enum):
    TRAINING = 'TRAINING'
    CANDIDATE = 'CANDIDATE'
    SHADOW = 'SHADOW'
    ACTIVE = 'ACTIVE'
    DEPRECATED = 'DEPRECATED'
    REVOKED = 'REVOKED'

class ActorKind(str, enum.Enum):
    HUMAN = 'HUMAN'
    SERVICE = 'SERVICE'
    SCHEDULED_JOB = 'SCHEDULED_JOB'

class AuditSeverity(str, enum.Enum):
    INFO = 'INFO'
    NOTICE = 'NOTICE'
    WARNING = 'WARNING'
    CRITICAL = 'CRITICAL'


# ==========================================
# 4. IDENTITY, RBAC & JURISDICTION
# ==========================================

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(UUID(as_uuid=True), primary_key=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))
    org_code = Column(Text, nullable=False, unique=True)
    display_name = Column(Text, nullable=False)
    org_type = Column(Text, nullable=False)
    state_code = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint('id <> parent_id', name='ck_org_no_self_parent'),
    )

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    external_subject_id = Column(Text, unique=True)
    username = Column(Text, nullable=False, unique=True)
    full_name = Column(Text, nullable=False)
    rank_designation = Column(Text, nullable=False)
    service_id_number = Column(Text)
    official_email = Column(Text, nullable=False)
    password_hash = Column(Text)
    mfa_enrolled = Column(Boolean, nullable=False, default=False)
    signing_key_ref = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    deactivated_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))
    failed_login_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint('external_subject_id IS NOT NULL OR password_hash IS NOT NULL', name='ck_users_auth_present'),
    )

class Role(Base):
    __tablename__ = 'roles'
    id = Column(SmallInteger, primary_key=True)
    role_code = Column(Text, nullable=False, unique=True)
    display_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    is_read_only = Column(Boolean, nullable=False, default=False)

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(SmallInteger, primary_key=True)
    permission_code = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    is_privileged = Column(Boolean, nullable=False, default=False)

class RolePermission(Base):
    __tablename__ = 'role_permissions'
    role_id = Column(SmallInteger, ForeignKey('roles.id'), primary_key=True)
    permission_id = Column(SmallInteger, ForeignKey('permissions.id'), primary_key=True)

class UserRole(Base):
    __tablename__ = 'user_roles'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    role_id = Column(SmallInteger, ForeignKey('roles.id'), primary_key=True)
    granted_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    granted_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_reauth_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    source_ip = Column(INET, nullable=False)
    user_agent_digest = Column(LargeBinary, nullable=False)
    mfa_satisfied = Column(Boolean, nullable=False, default=False)
    revoked_at = Column(DateTime(timezone=True))


# ==========================================
# 5. CASE MANAGEMENT
# ==========================================

class Case(Base):
    __tablename__ = 'cases'
    id = Column(UUID(as_uuid=True), primary_key=True)
    case_reference = Column(Text, nullable=False, unique=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    title = Column(Text, nullable=False)
    case_type = Column(String, nullable=False) # Enum CaseType
    status = Column(String, nullable=False, default=CaseStatus.DRAFT.value)
    priority = Column(SmallInteger, nullable=False, default=3)
    
    # Lawful Authority Gate
    fir_number = Column(Text)
    ncrp_acknowledgement = Column(Text)
    written_authority_ref = Column(Text)
    authority_recorded_at = Column(DateTime(timezone=True))
    authority_recorded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    reported_loss_base = Column(Numeric(78,0))
    reported_loss_currency = Column(String(3), default='INR')
    incident_occurred_at = Column(DateTime(timezone=True))
    complaint_filed_at = Column(DateTime(timezone=True))
    
    legal_hold = Column(Boolean, nullable=False, default=False)
    retention_expires_at = Column(DateTime(timezone=True))
    closed_at = Column(DateTime(timezone=True))
    closure_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        CheckConstraint(
            """status = 'DRAFT' OR fir_number IS NOT NULL OR ncrp_acknowledgement IS NOT NULL OR written_authority_ref IS NOT NULL""",
            name='ck_case_authority_present'
        ),
        CheckConstraint('priority BETWEEN 1 AND 5', name='ck_case_priority'),
        CheckConstraint("""(status IN ('CLOSED','ARCHIVED')) = (closed_at IS NOT NULL)""", name='ck_case_closed'),
    )

class CaseAccessGrant(Base):
    __tablename__ = 'case_access_grants'
    id = Column(UUID(as_uuid=True), primary_key=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), nullable=False)
    grantee_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    granted_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    justification = Column(Text, nullable=False)
    access_level = Column(Text, nullable=False)
    granted_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True))
    __table_args__ = (
        CheckConstraint('expires_at > granted_at', name='ck_grant_window'),
        CheckConstraint('length(justification) >= 20', name='ck_grant_justified'),
    )

class CaseSeedAddress(Base):
    __tablename__ = 'case_seed_addresses'
    id = Column(UUID(as_uuid=True), primary_key=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id', ondelete='RESTRICT'), nullable=False)
    # Forward ref to addresses
    address_id = Column(UUID(as_uuid=True), nullable=False)
    added_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    seed_role = Column(Text, nullable=False)
    source_of_address = Column(Text, nullable=False)
    notes = Column(Text)
    added_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        UniqueConstraint('case_id', 'address_id', name='ux_case_seed'),
    )

class CaseEvent(Base):
    __tablename__ = 'case_events'
    id = Column(UUID(as_uuid=True), primary_key=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), nullable=False)
    actor_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    actor_kind = Column(String, nullable=False, default=ActorKind.HUMAN.value)
    event_type = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    detail = Column(JSONB, nullable=False, server_default='{}')
    related_entity_type = Column(Text)
    related_entity_id = Column(UUID(as_uuid=True))
    occurred_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class CaseAttachment(Base):
    __tablename__ = 'case_attachments'
    id = Column(UUID(as_uuid=True), primary_key=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    file_name = Column(Text, nullable=False)
    mime_type = Column(Text, nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    sha256 = Column(LargeBinary, nullable=False)
    object_key = Column(Text, nullable=False)
    virus_scan_status = Column(Text, nullable=False, default='PENDING')
    uploaded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint('size_bytes > 0', name='ck_attach_size'),
        CheckConstraint('octet_length(sha256) = 32', name='ck_attach_hash'),
    )

# ==========================================
# 6. CHAIN & ASSET REFERENCE DATA
# ==========================================

class Chain(Base):
    __tablename__ = 'chains'
    id = Column(SmallInteger, primary_key=True)
    chain_key = Column(Text, nullable=False, unique=True)
    display_name = Column(Text, nullable=False)
    chain_model = Column(String, nullable=False) # Enum ChainModel
    native_asset_symbol = Column(Text, nullable=False)
    caip2_identifier = Column(Text)
    address_regex = Column(Text, nullable=False)
    address_checksum_scheme = Column(Text, nullable=False)
    explorer_url_template = Column(Text, nullable=False)
    graph_shard_key = Column(Text, nullable=False)
    proof_kind = Column(String, nullable=False) # Enum ProofKind
    is_enabled = Column(Boolean, nullable=False, default=True)
    added_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class ChainFinalityConfig(Base):
    __tablename__ = 'chain_finality_configs'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chain_id = Column(SmallInteger, ForeignKey('chains.id'), nullable=False)
    min_confirmations = Column(Integer, nullable=False)
    finality_semantics = Column(Text, nullable=False)
    notes = Column(Text)
    effective_from = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    effective_to = Column(DateTime(timezone=True))
    set_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    __table_args__ = (
        CheckConstraint('min_confirmations >= 0', name='ck_finality_positive'),
        CheckConstraint('effective_to IS NULL OR effective_to > effective_from', name='ck_finality_window'),
    )

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chain_id = Column(SmallInteger, ForeignKey('chains.id'), nullable=False)
    contract_address_canon = Column(Text)
    symbol = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    decimals = Column(SmallInteger, nullable=False)
    token_standard = Column(Text)
    is_stablecoin = Column(Boolean, nullable=False, default=False)
    dust_threshold_base = Column(Numeric(78,0))
    is_verified = Column(Boolean, nullable=False, default=False)
    first_seen_at = Column(DateTime(timezone=True))
    __table_args__ = (
        UniqueConstraint('chain_id', 'contract_address_canon', name='ux_assets_chain_addr'),
        CheckConstraint('decimals BETWEEN 0 AND 36', name='ck_assets_decimals'),
    )

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chain_id = Column(SmallInteger, ForeignKey('chains.id'), nullable=False)
    address_canonical = Column(Text, nullable=False)
    address_raw_first_seen = Column(Text, nullable=False)
    is_contract = Column(Boolean)
    contract_bytecode_hash = Column(LargeBinary)
    contract_created_at_blk = Column(BigInteger)
    first_activity_at = Column(DateTime(timezone=True))
    last_activity_at = Column(DateTime(timezone=True))
    tx_count_cached = Column(BigInteger, nullable=False, default=0)
    degree_in_cached = Column(BigInteger, nullable=False, default=0)
    degree_out_cached = Column(BigInteger, nullable=False, default=0)
    is_high_degree = Column(Boolean, nullable=False, default=False)
    cache_refreshed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        UniqueConstraint('chain_id', 'address_canonical', name='ux_addresses_chain_addr'),
    )

class ContractSignature(Base):
    __tablename__ = 'contract_signatures'
    id = Column(UUID(as_uuid=True), primary_key=True)
    signature_family = Column(Text, nullable=False)
    expected_class = Column(String, nullable=False) # NodeClass
    match_kind = Column(Text, nullable=False)
    match_value = Column(Text, nullable=False)
    confidence_weight = Column(Numeric(4,3), nullable=False, default=0.900)
    source_reference = Column(Text, nullable=False)
    added_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    added_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    is_active = Column(Boolean, nullable=False, default=True)
    __table_args__ = (
        CheckConstraint('confidence_weight BETWEEN 0 AND 1', name='ck_sig_weight'),
    )

# ==========================================
# 7. CANONICAL LEDGER FACTS
# ==========================================

class Block(Base):
    __tablename__ = 'blocks'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chain_id = Column(SmallInteger, ForeignKey('chains.id'), primary_key=True, nullable=False)
    block_height = Column(BigInteger, nullable=False)
    block_hash = Column(LargeBinary, nullable=False)
    parent_block_hash = Column(LargeBinary)
    merkle_root = Column(LargeBinary)
    state_root = Column(LargeBinary)
    receipts_root = Column(LargeBinary)
    block_timestamp = Column(DateTime(timezone=True), nullable=False)
    tx_count = Column(Integer, nullable=False, default=0)
    is_orphaned = Column(Boolean, nullable=False, default=False)
    orphaned_detected_at = Column(DateTime(timezone=True))
    ingest_run_id = Column(UUID(as_uuid=True), nullable=False)
    ingested_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        {'postgresql_partition_by': 'LIST (chain_id)'}
    )

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chain_id = Column(SmallInteger, primary_key=True, nullable=False)
    tx_hash = Column(LargeBinary, nullable=False)
    block_height = Column(BigInteger, nullable=False)
    block_hash = Column(LargeBinary, nullable=False)
    tx_index_in_block = Column(Integer)
    block_timestamp = Column(DateTime(timezone=True), nullable=False)
    
    from_address_id = Column(UUID(as_uuid=True))
    to_address_id = Column(UUID(as_uuid=True))
    nonce = Column(BigInteger)
    is_contract_creation = Column(Boolean, nullable=False, default=False)
    input_selector = Column(LargeBinary)
    status_success = Column(Boolean)
    
    input_count = Column(Integer)
    output_count = Column(Integer)
    is_coinbase = Column(Boolean, nullable=False, default=False)
    
    fee_base = Column(Numeric(78,0))
    confirmations_at_ingest = Column(Integer)
    validation_status = Column(String, nullable=False, default=ValidationStatus.UNVERIFIED.value)
    source_count = Column(SmallInteger, nullable=False, default=0)
    canonical_digest = Column(LargeBinary, nullable=False)
    ingest_run_id = Column(UUID(as_uuid=True), nullable=False)
    ingested_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        CheckConstraint(
            """(input_count IS NOT NULL) OR (from_address_id IS NOT NULL) OR is_coinbase""",
            name='ck_tx_model_fields'
        ),
        {'postgresql_partition_by': 'LIST (chain_id)'}
    )

class Transfer(Base):
    __tablename__ = 'transfers'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chain_id = Column(SmallInteger, primary_key=True, nullable=False)
    transaction_id = Column(UUID(as_uuid=True), nullable=False)
    tx_hash = Column(LargeBinary, nullable=False)
    block_height = Column(BigInteger, nullable=False)
    block_timestamp = Column(DateTime(timezone=True), nullable=False)
    
    transfer_index = Column(Integer, nullable=False)
    transfer_kind = Column(Text, nullable=False)
    from_address_id = Column(UUID(as_uuid=True))
    to_address_id = Column(UUID(as_uuid=True))
    asset_id = Column(UUID(as_uuid=True), nullable=False)
    value_base = Column(Numeric(78,0), nullable=False)
    
    utxo_spent_tx_hash = Column(LargeBinary)
    utxo_spent_vout = Column(Integer)
    utxo_created_vout = Column(Integer)
    
    is_change_output = Column(Boolean)
    change_heuristic = Column(Text)
    cospend_cluster_id = Column(UUID(as_uuid=True))
    
    validation_status = Column(String, nullable=False, default=ValidationStatus.UNVERIFIED.value)
    is_pruned = Column(Boolean, nullable=False, default=False)
    prune_reason = Column(Text)
    ingest_run_id = Column(UUID(as_uuid=True), nullable=False)
    ingested_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        CheckConstraint('value_base >= 0', name='ck_transfer_value_nonneg'),
        CheckConstraint('from_address_id IS NOT NULL OR to_address_id IS NOT NULL', name='ck_transfer_endpoints'),
        CheckConstraint('(is_pruned = FALSE) OR (prune_reason IS NOT NULL)', name='ck_prune_reason'),
        {'postgresql_partition_by': 'LIST (chain_id)'}
    )

class CospendCluster(Base):
    __tablename__ = 'cospend_clusters'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chain_id = Column(SmallInteger, ForeignKey('chains.id'), nullable=False)
    member_count = Column(Integer, nullable=False)
    representative_addr_id = Column(UUID(as_uuid=True), nullable=False)
    heuristic_version = Column(Text, nullable=False)
    computed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    ingest_run_id = Column(UUID(as_uuid=True), nullable=False)

class CospendClusterMember(Base):
    __tablename__ = 'cospend_cluster_members'
    cluster_id = Column(UUID(as_uuid=True), ForeignKey('cospend_clusters.id'), primary_key=True)
    address_id = Column(UUID(as_uuid=True), primary_key=True)
    evidence_tx_hash = Column(LargeBinary, nullable=False)

# ==========================================
# 8. PROVENANCE & CROSS-VALIDATION
# ==========================================

class DataProvider(Base):
    __tablename__ = 'data_providers'
    id = Column(SmallInteger, primary_key=True)
    provider_key = Column(Text, nullable=False, unique=True)
    display_name = Column(Text, nullable=False)
    base_url = Column(Text, nullable=False)
    supported_chain_ids = Column(ARRAY(SmallInteger), nullable=False)
    rate_limit_per_sec = Column(Numeric(8,3))
    rate_limit_per_day = Column(BigInteger)
    is_self_hosted = Column(Boolean, nullable=False, default=False)
    leaks_query_interest = Column(Boolean, nullable=False, default=True)
    is_enabled = Column(Boolean, nullable=False, default=True)
    priority_rank = Column(SmallInteger, nullable=False, default=100)

class ProviderHealth(Base):
    __tablename__ = 'provider_health'
    id = Column(UUID(as_uuid=True), primary_key=True)
    provider_id = Column(SmallInteger, ForeignKey('data_providers.id'), nullable=False)
    window_start = Column(DateTime(timezone=True), nullable=False)
    window_end = Column(DateTime(timezone=True), nullable=False)
    request_count = Column(BigInteger, nullable=False, default=0)
    success_count = Column(BigInteger, nullable=False, default=0)
    error_count = Column(BigInteger, nullable=False, default=0)
    timeout_count = Column(BigInteger, nullable=False, default=0)
    disagreement_count = Column(BigInteger, nullable=False, default=0)
    p50_latency_ms = Column(Integer)
    p95_latency_ms = Column(Integer)
    health_score = Column(Numeric(4,3))
    __table_args__ = (
        UniqueConstraint('provider_id', 'window_start', name='ux_provider_health_window'),
    )

class TransactionSource(Base):
    __tablename__ = 'transaction_sources'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chain_id = Column(SmallInteger, nullable=False)
    transaction_id = Column(UUID(as_uuid=True), nullable=False)
    tx_hash = Column(LargeBinary, nullable=False)
    provider_id = Column(SmallInteger, ForeignKey('data_providers.id'), nullable=False)
    fetched_at = Column(DateTime(timezone=True), nullable=False)
    http_status = Column(Integer)
    response_digest = Column(LargeBinary, nullable=False)
    canonical_digest = Column(LargeBinary, nullable=False)
    raw_payload_object_key = Column(Text)
    agrees_with_consensus = Column(Boolean)
    disagreement_fields = Column(ARRAY(Text))
    ingest_run_id = Column(UUID(as_uuid=True), nullable=False)
    __table_args__ = (
        UniqueConstraint('chain_id', 'tx_hash', 'provider_id', 'fetched_at', name='ux_tx_source'),
    )

class IngestRun(Base):
    __tablename__ = 'ingest_runs'
    id = Column(UUID(as_uuid=True), primary_key=True)
    trace_id = Column(UUID(as_uuid=True))
    triggered_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    trigger_kind = Column(Text, nullable=False)
    chain_id = Column(SmallInteger, ForeignKey('chains.id'))
    started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    finished_at = Column(DateTime(timezone=True))
    addresses_touched = Column(Integer, nullable=False, default=0)
    transactions_ingested = Column(Integer, nullable=False, default=0)
    transfers_ingested = Column(Integer, nullable=False, default=0)
    provider_calls = Column(Integer, nullable=False, default=0)
    conflicts_detected = Column(Integer, nullable=False, default=0)
    status = Column(Text, nullable=False, default='RUNNING')
    error_detail = Column(JSONB)

# ==========================================
# 9. TEMPORAL ANALYSIS
# ==========================================

class TemporalProfile(Base):
    __tablename__ = 'temporal_profiles'
    id = Column(UUID(as_uuid=True), primary_key=True)
    address_id = Column(UUID(as_uuid=True), nullable=False)
    chain_id = Column(SmallInteger, nullable=False)
    trace_id = Column(UUID(as_uuid=True))
    model_version_id = Column(UUID(as_uuid=True), nullable=False)
    
    hawkes_mu = Column(Float)
    hawkes_alpha = Column(Float)
    hawkes_beta = Column(Float)
    branching_ratio = Column(Float)
    log_likelihood = Column(Float)
    fit_event_count = Column(Integer, nullable=False)
    fit_window_start = Column(DateTime(timezone=True))
    fit_window_end = Column(DateTime(timezone=True))
    
    dominant_pattern = Column(String, nullable=False) # Enum TemporalPattern
    pattern_scores = Column(JSONB, nullable=False)
    burst_count = Column(Integer, nullable=False, default=0)
    median_interarrival_s = Column(Float)
    interarrival_cv = Column(Float)
    
    computed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    parameters_json = Column(JSONB, nullable=False)
    __table_args__ = (
        CheckConstraint('branching_ratio IS NULL OR branching_ratio >= 0', name='ck_branching'),
    )

class TemporalBurst(Base):
    __tablename__ = 'temporal_bursts'
    id = Column(UUID(as_uuid=True), primary_key=True)
    temporal_profile_id = Column(UUID(as_uuid=True), ForeignKey('temporal_profiles.id'), nullable=False)
    burst_start_at = Column(DateTime(timezone=True), nullable=False)
    burst_end_at = Column(DateTime(timezone=True), nullable=False)
    event_count = Column(Integer, nullable=False)
    peak_intensity = Column(Float)
    total_value_base = Column(Numeric(78,0))
    pattern = Column(String, nullable=False) # Enum TemporalPattern
    __table_args__ = (
        CheckConstraint('burst_end_at >= burst_start_at', name='ck_burst_window'),
    )

# ==========================================
# 10. CLASSIFICATION ARTEFACTS
# ==========================================

class AddressClassification(Base):
    __tablename__ = 'address_classifications'
    id = Column(UUID(as_uuid=True), primary_key=True)
    address_id = Column(UUID(as_uuid=True), nullable=False)
    chain_id = Column(SmallInteger, nullable=False)
    trace_id = Column(UUID(as_uuid=True))
    
    predicted_class = Column(String, nullable=False) # Enum NodeClass
    class_probabilities = Column(JSONB, nullable=False)
    max_probability = Column(Numeric(5,4), nullable=False)
    is_abstained = Column(Boolean, nullable=False, default=False)
    is_absorption_state = Column(Boolean, nullable=False, default=False)
    
    hgt_model_version_id = Column(UUID(as_uuid=True))
    rgcn_model_version_id = Column(UUID(as_uuid=True))
    tgn_model_version_id = Column(UUID(as_uuid=True))
    calibrator_version_id = Column(UUID(as_uuid=True))
    feature_set_version = Column(Text, nullable=False)
    
    bytecode_signature_id = Column(UUID(as_uuid=True), ForeignKey('contract_signatures.id'))
    registry_match_vasp_id = Column(UUID(as_uuid=True))
    external_label_source = Column(Text)
    
    top_features = Column(JSONB)
    attention_summary = Column(JSONB)
    
    is_human_override = Column(Boolean, nullable=False, default=False)
    overridden_from_class = Column(String) # NodeClass
    override_justification = Column(Text)
    overridden_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    overridden_at = Column(DateTime(timezone=True))
    
    superseded_by_id = Column(UUID(as_uuid=True), ForeignKey('address_classifications.id'))
    computed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        CheckConstraint('max_probability BETWEEN 0 AND 1', name='ck_cls_prob'),
        CheckConstraint("""(is_abstained = FALSE) OR (predicted_class = 'UNKNOWN')""", name='ck_cls_abstain'),
        CheckConstraint(
            """(is_human_override = FALSE) OR
            (override_justification IS NOT NULL
            AND length(override_justification) >= 20
            AND overridden_by IS NOT NULL
            AND overridden_from_class IS NOT NULL)""",
            name='ck_cls_override'
        ),
    )

class ClassificationLabelCandidate(Base):
    __tablename__ = 'classification_label_candidates'
    id = Column(UUID(as_uuid=True), primary_key=True)
    classification_id = Column(UUID(as_uuid=True), ForeignKey('address_classifications.id'), nullable=False)
    proposed_label = Column(String, nullable=False) # NodeClass
    proposed_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    proposed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    curator_status = Column(Text, nullable=False, default='PENDING')
    curator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    curator_note = Column(Text)
    reviewed_at = Column(DateTime(timezone=True))
    included_in_dataset = Column(Text)

# ==========================================
# 11. TRACE, PATH & CONFIDENCE
# ==========================================

class Trace(Base):
    __tablename__ = 'traces'
    id = Column(UUID(as_uuid=True), primary_key=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), nullable=False)
    seed_address_id = Column(UUID(as_uuid=True), nullable=False)
    chain_id = Column(SmallInteger, ForeignKey('chains.id'), nullable=False)
    launched_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    status = Column(String, nullable=False, default=TraceStatus.QUEUED.value)
    termination_reason = Column(Text)
    
    graph_snapshot_id = Column(UUID(as_uuid=True), nullable=False)
    rng_seed = Column(BigInteger, nullable=False)
    parameter_set = Column(JSONB, nullable=False)
    model_version_pins = Column(JSONB, nullable=False)
    engine_version = Column(Text, nullable=False)
    
    max_depth = Column(Integer, nullable=False, default=12)
    top_k_paths = Column(Integer, nullable=False, default=3)
    value_floor_fraction = Column(Numeric(5,4), nullable=False, default=0.0100)
    time_budget_ms = Column(Integer, nullable=False, default=300000)
    pruning_enabled = Column(Boolean, nullable=False, default=True)
    opsec_mode = Column(Boolean, nullable=False, default=False)
    
    nodes_expanded = Column(Integer)
    edges_examined = Column(BigInteger)
    provider_calls = Column(Integer)
    cache_hit_ratio = Column(Numeric(5,4))
    
    queued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_ms = Column(Integer)
    error_detail = Column(JSONB)
    
    parent_trace_id = Column(UUID(as_uuid=True), ForeignKey('traces.id'))
    rerun_reason = Column(Text)
    
    __table_args__ = (
        CheckConstraint('max_depth BETWEEN 1 AND 30', name='ck_trace_depth'),
        CheckConstraint('top_k_paths BETWEEN 1 AND 10', name='ck_trace_topk'),
    )

class TraceStage(Base):
    __tablename__ = 'trace_stages'
    id = Column(UUID(as_uuid=True), primary_key=True)
    trace_id = Column(UUID(as_uuid=True), ForeignKey('traces.id'), nullable=False)
    stage_name = Column(Text, nullable=False)
    stage_order = Column(SmallInteger, nullable=False)
    status = Column(Text, nullable=False)
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
    duration_ms = Column(Integer)
    items_processed = Column(Integer)
    metrics = Column(JSONB, nullable=False, server_default='{}')
    error_detail = Column(JSONB)
    __table_args__ = (
        UniqueConstraint('trace_id', 'stage_name', name='ux_trace_stage'),
    )

class TracePath(Base):
    __tablename__ = 'trace_paths'
    id = Column(UUID(as_uuid=True), primary_key=True)
    trace_id = Column(UUID(as_uuid=True), ForeignKey('traces.id'), nullable=False)
    rank = Column(SmallInteger, nullable=False)
    hop_count = Column(SmallInteger, nullable=False)
    
    terminal_address_id = Column(UUID(as_uuid=True), nullable=False)
    terminal_class = Column(String, nullable=False) # NodeClass
    terminal_vasp_id = Column(UUID(as_uuid=True))
    jurisdiction = Column(String, nullable=False, default=Jurisdiction.UNKNOWN_ENTITY.value)
    
    traced_value_base = Column(Numeric(78,0), nullable=False)
    traced_value_asset_id = Column(UUID(as_uuid=True), nullable=False)
    value_fraction_of_seed = Column(Numeric(6,5))
    attribution_method = Column(Text, nullable=False)
    elapsed_onchain_seconds = Column(BigInteger)
    
    crosses_chains = Column(Boolean, nullable=False, default=False)
    crosses_mixer = Column(Boolean, nullable=False, default=False)
    crosses_bridge = Column(Boolean, nullable=False, default=False)
    
    is_selected = Column(Boolean, nullable=False, default=False)
    selected_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    selected_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('trace_id', 'rank', name='ux_trace_path_rank'),
        CheckConstraint('hop_count > 0', name='ck_path_hops'),
    )

class TracePathHop(Base):
    __tablename__ = 'trace_path_hops'
    id = Column(UUID(as_uuid=True), primary_key=True)
    trace_path_id = Column(UUID(as_uuid=True), ForeignKey('trace_paths.id'), nullable=False)
    hop_index = Column(SmallInteger, nullable=False)
    
    from_address_id = Column(UUID(as_uuid=True), nullable=False)
    to_address_id = Column(UUID(as_uuid=True), nullable=False)
    chain_id = Column(SmallInteger, nullable=False)
    
    transfer_id = Column(UUID(as_uuid=True))
    tx_hash = Column(LargeBinary, nullable=False)
    block_height = Column(BigInteger, nullable=False)
    block_timestamp = Column(DateTime(timezone=True), nullable=False)
    asset_id = Column(UUID(as_uuid=True), nullable=False)
    value_base = Column(Numeric(78,0), nullable=False)
    
    edge_weight = Column(Float)
    time_decay_factor = Column(Float)
    value_share = Column(Numeric(6,5))
    from_classification_id = Column(UUID(as_uuid=True), ForeignKey('address_classifications.id'))
    to_classification_id = Column(UUID(as_uuid=True), ForeignKey('address_classifications.id'))
    temporal_pattern = Column(String) # TemporalPattern
    validation_status = Column(String, nullable=False) # ValidationStatus
    confirmations_observed = Column(Integer)
    
    is_cross_chain_hop = Column(Boolean, nullable=False, default=False)
    bridge_contract_addr_id = Column(UUID(as_uuid=True))
    counterpart_chain_id = Column(SmallInteger)
    
    hop_note = Column(Text)
    __table_args__ = (
        UniqueConstraint('trace_path_id', 'hop_index', name='ux_trace_path_hop'),
    )

class ConfidenceScore(Base):
    __tablename__ = 'confidence_scores'
    id = Column(UUID(as_uuid=True), primary_key=True)
    trace_path_id = Column(UUID(as_uuid=True), ForeignKey('trace_paths.id'), nullable=False)
    
    point_estimate = Column(Numeric(6,5), nullable=False)
    ci_lower = Column(Numeric(6,5), nullable=False)
    ci_upper = Column(Numeric(6,5), nullable=False)
    ci_level = Column(Numeric(4,3), nullable=False, default=0.950)
    
    mc_sample_count = Column(Integer, nullable=False)
    mc_restart_probability = Column(Numeric(4,3), nullable=False)
    mc_converged = Column(Boolean, nullable=False)
    mc_seed = Column(BigInteger, nullable=False)
    
    factor_classification = Column(Numeric(6,5))
    factor_corroboration = Column(Numeric(6,5))
    factor_temporal = Column(Numeric(6,5))
    factor_path_length = Column(Numeric(6,5))
    factor_obfuscation = Column(Numeric(6,5))
    factor_json = Column(JSONB, nullable=False, server_default='{}')
    
    calibrator_version_id = Column(UUID(as_uuid=True))
    meets_action_threshold = Column(Boolean, nullable=False)
    action_threshold_used = Column(Numeric(4,3), nullable=False)
    
    computed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('trace_path_id', name='ux_conf_path'),
        CheckConstraint('point_estimate BETWEEN 0 AND 1', name='ck_conf_range'),
        CheckConstraint('ci_lower <= point_estimate AND point_estimate <= ci_upper', name='ck_conf_ci'),
        CheckConstraint('mc_sample_count >= 1000', name='ck_conf_samples'),
    )

class ObfuscationCorrelation(Base):
    __tablename__ = 'obfuscation_correlations'
    id = Column(UUID(as_uuid=True), primary_key=True)
    trace_id = Column(UUID(as_uuid=True), ForeignKey('traces.id'), nullable=False)
    obfuscator_address_id = Column(UUID(as_uuid=True), nullable=False)
    obfuscator_kind = Column(String, nullable=False) # NodeClass
    deposit_tx_hash = Column(LargeBinary, nullable=False)
    deposit_at = Column(DateTime(timezone=True), nullable=False)
    deposit_value_base = Column(Numeric(78,0), nullable=False)
    deposit_asset_id = Column(UUID(as_uuid=True), nullable=False)
    
    candidate_address_id = Column(UUID(as_uuid=True), nullable=False)
    candidate_tx_hash = Column(LargeBinary, nullable=False)
    candidate_at = Column(DateTime(timezone=True), nullable=False)
    candidate_value_base = Column(Numeric(78,0), nullable=False)
    
    time_delta_seconds = Column(BigInteger, nullable=False)
    denomination_match = Column(Boolean, nullable=False)
    correlation_score = Column(Numeric(6,5), nullable=False)
    anonymity_set_estimate = Column(Integer)
    is_actionable = Column(Boolean, nullable=False, default=False)
    computed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint('correlation_score BETWEEN 0 AND 1', name='ck_corr_score'),
    )

# ==========================================
# 12. MERKLE PROOFS & EVIDENCE
# ==========================================

class MerkleProof(Base):
    __tablename__ = 'merkle_proofs'
    id = Column(UUID(as_uuid=True), primary_key=True)
    chain_id = Column(SmallInteger, ForeignKey('chains.id'), nullable=False)
    tx_hash = Column(LargeBinary, nullable=False)
    block_height = Column(BigInteger, nullable=False)
    block_hash = Column(LargeBinary, nullable=False)
    merkle_root = Column(LargeBinary)
    
    proof_kind = Column(String, nullable=False) # Enum ProofKind
    hash_algorithm = Column(Text, nullable=False)
    leaf_hash = Column(LargeBinary, nullable=False)
    leaf_index = Column(Integer)
    
    proof_path = Column(JSONB, nullable=False)
    proof_depth = Column(SmallInteger, nullable=False)
    
    verification_status = Column(String, nullable=False, default=ProofStatus.PENDING.value)
    verified_at = Column(DateTime(timezone=True))
    verified_root = Column(LargeBinary)
    verification_note = Column(Text)
    
    alternative_mechanism = Column(Text)
    source_provider_id = Column(SmallInteger, ForeignKey('data_providers.id'))
    fetched_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('chain_id', 'tx_hash', 'proof_kind', name='ux_merkle_tx_proof'),
        CheckConstraint('proof_depth >= 0', name='ck_proof_depth'),
        CheckConstraint(
            """proof_kind <> 'HEADER_ANCHORED_DIGEST' OR alternative_mechanism IS NOT NULL""",
            name='ck_proof_alt'
        ),
    )

class EvidenceItem(Base):
    __tablename__ = 'evidence_items'
    id = Column(UUID(as_uuid=True), primary_key=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), nullable=False)
    trace_id = Column(UUID(as_uuid=True), ForeignKey('traces.id'))
    trace_path_hop_id = Column(UUID(as_uuid=True), ForeignKey('trace_path_hops.id'))
    
    evidence_kind = Column(Text, nullable=False)
    chain_id = Column(SmallInteger)
    tx_hash = Column(LargeBinary)
    merkle_proof_id = Column(UUID(as_uuid=True), ForeignKey('merkle_proofs.id'))
    
    content_digest = Column(LargeBinary, nullable=False)
    payload_snapshot = Column(JSONB, nullable=False)
    object_key = Column(Text)
    
    collected_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    collected_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    collection_method = Column(Text, nullable=False)
    sealed_at = Column(DateTime(timezone=True))
    
    __table_args__ = (
        CheckConstraint('octet_length(content_digest) = 32', name='ck_evidence_digest'),
    )

class ChainOfCustody(Base):
    __tablename__ = 'chain_of_custody'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    evidence_item_id = Column(UUID(as_uuid=True), ForeignKey('evidence_items.id'), nullable=False)
    actor_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    actor_kind = Column(String, nullable=False) # Enum ActorKind
    action = Column(Text, nullable=False)
    transformation_detail = Column(JSONB)
    source_ip = Column(INET)
    occurred_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

# ==========================================
# 13. VASP REGISTRY
# ==========================================

class VaspEntity(Base):
    __tablename__ = 'vasp_entities'
    id = Column(UUID(as_uuid=True), primary_key=True)
    legal_name = Column(Text, nullable=False)
    trading_name = Column(Text)
    entity_type = Column(Text, nullable=False)
    country_code = Column(String(2), nullable=False)
    website = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class VaspRegistration(Base):
    __tablename__ = 'vasp_registrations'
    id = Column(UUID(as_uuid=True), primary_key=True)
    vasp_entity_id = Column(UUID(as_uuid=True), ForeignKey('vasp_entities.id'), nullable=False)
    registry_authority = Column(Text, nullable=False)
    registration_id = Column(Text)
    jurisdiction = Column(String, nullable=False) # Enum Jurisdiction
    is_sahyog_onboarded = Column(Boolean, nullable=False, default=False)
    sahyog_onboarded_at = Column(Date)
    accepts_legal_basis = Column(ARRAY(String), nullable=False, server_default='{}')
    
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date)
    recorded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    superseded_at = Column(DateTime(timezone=True))
    source_reference = Column(Text, nullable=False)
    source_verified_on = Column(Date, nullable=False)
    recorded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    __table_args__ = (
        CheckConstraint('valid_to IS NULL OR valid_to > valid_from', name='ck_vasp_valid_window'),
    )

class VaspNodalOfficer(Base):
    __tablename__ = 'vasp_nodal_officers'
    id = Column(UUID(as_uuid=True), primary_key=True)
    vasp_entity_id = Column(UUID(as_uuid=True), ForeignKey('vasp_entities.id'), nullable=False)
    officer_name = Column(Text, nullable=False)
    designation = Column(Text)
    official_email = Column(Text)
    phone = Column(Text)
    postal_address = Column(Text)
    preferred_channel = Column(Text, nullable=False)
    sahyog_endpoint_ref = Column(Text)
    is_primary = Column(Boolean, nullable=False, default=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date)
    source_reference = Column(Text, nullable=False)
    recorded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    recorded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class VaspAddress(Base):
    __tablename__ = 'vasp_addresses'
    id = Column(UUID(as_uuid=True), primary_key=True)
    vasp_entity_id = Column(UUID(as_uuid=True), ForeignKey('vasp_entities.id'), nullable=False)
    address_id = Column(UUID(as_uuid=True), nullable=False)
    chain_id = Column(SmallInteger, nullable=False)
    address_role = Column(String, nullable=False) # Enum NodeClass
    attribution_source = Column(Text, nullable=False)
    attribution_confidence = Column(Numeric(4,3), nullable=False)
    evidence_reference = Column(Text)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date)
    recorded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    recorded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        UniqueConstraint('address_id', 'vasp_entity_id', 'valid_from', name='ux_vasp_address'),
        CheckConstraint('attribution_confidence BETWEEN 0 AND 1', name='ck_vaspaddr_conf'),
    )

class BridgeIndex(Base):
    __tablename__ = 'bridge_index'
    id = Column(UUID(as_uuid=True), primary_key=True)
    bridge_protocol = Column(Text, nullable=False)
    source_chain_id = Column(SmallInteger, ForeignKey('chains.id'), nullable=False)
    source_address_id = Column(UUID(as_uuid=True), nullable=False)
    dest_chain_id = Column(SmallInteger, ForeignKey('chains.id'), nullable=False)
    dest_address_id = Column(UUID(as_uuid=True), nullable=False)
    correlation_method = Column(Text, nullable=False)
    typical_latency_seconds = Column(Integer)
    is_active = Column(Boolean, nullable=False, default=True)
    source_reference = Column(Text, nullable=False)
    recorded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    recorded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        UniqueConstraint('source_chain_id', 'source_address_id', 'dest_chain_id', 'dest_address_id', name='ux_bridge_index'),
    )

# ==========================================
# 14. DOSSIERS & LEGAL INSTRUMENTS
# ==========================================

class Dossier(Base):
    __tablename__ = 'dossiers'
    id = Column(UUID(as_uuid=True), primary_key=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), nullable=False)
    trace_id = Column(UUID(as_uuid=True), ForeignKey('traces.id'), nullable=False)
    trace_path_id = Column(UUID(as_uuid=True), ForeignKey('trace_paths.id'), nullable=False)
    
    dossier_number = Column(Text, nullable=False, unique=True)
    version = Column(Integer, nullable=False, default=1)
    supersedes_dossier_id = Column(UUID(as_uuid=True), ForeignKey('dossiers.id'))
    supersede_reason = Column(Text)
    
    template_version = Column(Text, nullable=False)
    language = Column(Text, nullable=False, default='en')
    
    pdf_object_key = Column(Text, nullable=False)
    pdf_sha256 = Column(LargeBinary, nullable=False)
    pdf_size_bytes = Column(BigInteger, nullable=False)
    json_bundle_object_key = Column(Text)
    json_bundle_sha256 = Column(LargeBinary)
    
    certificate_form = Column(Text, nullable=False)
    certifying_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    certifying_rank = Column(Text)
    certified_at = Column(DateTime(timezone=True))
    
    confidence_at_generation = Column(Numeric(6,5), nullable=False)
    hop_count = Column(SmallInteger, nullable=False)
    evidence_item_count = Column(Integer, nullable=False)
    proofs_verified_count = Column(Integer, nullable=False)
    proofs_failed_count = Column(Integer, nullable=False, default=0)
    
    is_superseded = Column(Boolean, nullable=False, default=False)
    invalidated_at = Column(DateTime(timezone=True))
    invalidation_reason = Column(Text)
    
    generated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    generated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        CheckConstraint('octet_length(pdf_sha256) = 32', name='ck_dossier_hash'),
        CheckConstraint('(supersedes_dossier_id IS NULL) = (supersede_reason IS NULL)', name='ck_dossier_supersede'),
    )

class DossierEvidenceItem(Base):
    __tablename__ = 'dossier_evidence_items'
    dossier_id = Column(UUID(as_uuid=True), ForeignKey('dossiers.id'), primary_key=True)
    evidence_item_id = Column(UUID(as_uuid=True), ForeignKey('evidence_items.id'), primary_key=True)
    display_order = Column(Integer, nullable=False)
    section = Column(Text, nullable=False)

class DossierSignature(Base):
    __tablename__ = 'dossier_signatures'
    id = Column(UUID(as_uuid=True), primary_key=True)
    dossier_id = Column(UUID(as_uuid=True), ForeignKey('dossiers.id'), nullable=False)
    signer_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    signer_role = Column(Text, nullable=False)
    signature_algorithm = Column(Text, nullable=False)
    signature_value = Column(LargeBinary, nullable=False)
    certificate_ref = Column(Text, nullable=False)
    signed_digest = Column(LargeBinary, nullable=False)
    mfa_method = Column(Text, nullable=False)
    signed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    source_ip = Column(INET, nullable=False)

class DisclosureRequest(Base):
    __tablename__ = 'disclosure_requests'
    id = Column(UUID(as_uuid=True), primary_key=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id'), nullable=False)
    dossier_id = Column(UUID(as_uuid=True), ForeignKey('dossiers.id'), nullable=False)
    trace_path_id = Column(UUID(as_uuid=True), ForeignKey('trace_paths.id'), nullable=False)
    vasp_entity_id = Column(UUID(as_uuid=True), ForeignKey('vasp_entities.id'), nullable=False)
    nodal_officer_id = Column(UUID(as_uuid=True), ForeignKey('vasp_nodal_officers.id'))
    
    request_reference = Column(Text, nullable=False, unique=True)
    legal_basis = Column(String, nullable=False) # Enum LegalBasis
    status = Column(String, nullable=False, default=DisclosureStatus.DRAFT.value)
    
    target_address_id = Column(UUID(as_uuid=True), nullable=False)
    target_tx_hashes = Column(ARRAY(LargeBinary), nullable=False)
    time_window_start = Column(DateTime(timezone=True), nullable=False)
    time_window_end = Column(DateTime(timezone=True), nullable=False)
    requested_data_types = Column(ARRAY(Text), nullable=False)
    freeze_requested = Column(Boolean, nullable=False, default=False)
    freeze_amount_base = Column(Numeric(78,0))
    
    scope_check_passed = Column(Boolean, nullable=False, default=False)
    scope_check_detail = Column(JSONB)
    
    is_mock_environment = Column(Boolean, nullable=False, default=True)
    sahyog_submission_id = Column(Text)
    idempotency_key = Column(Text, nullable=False, unique=True)
    submitted_at = Column(DateTime(timezone=True))
    acknowledged_at = Column(DateTime(timezone=True))
    responded_at = Column(DateTime(timezone=True))
    sla_due_at = Column(DateTime(timezone=True))
    
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    approved_at = Column(DateTime(timezone=True))
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        CheckConstraint('time_window_end > time_window_start', name='ck_disc_window'),
        CheckConstraint('array_length(target_tx_hashes, 1) >= 1', name='ck_disc_targets'),
        CheckConstraint(
            """status NOT IN ('SIGNED','SUBMITTED','ACKNOWLEDGED','RESPONDED') OR (approved_by IS NOT NULL AND scope_check_passed = TRUE)""",
            name='ck_disc_dispatch_gate'
        ),
    )

class DisclosureRequestField(Base):
    __tablename__ = 'disclosure_request_fields'
    id = Column(UUID(as_uuid=True), primary_key=True)
    disclosure_request_id = Column(UUID(as_uuid=True), ForeignKey('disclosure_requests.id'), nullable=False)
    field_key = Column(Text, nullable=False)
    machine_value = Column(Text)
    final_value = Column(Text)
    was_edited = Column(Boolean, nullable=False, default=False)
    edited_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    edited_at = Column(DateTime(timezone=True))
    provenance = Column(JSONB, nullable=False)
    __table_args__ = (
        UniqueConstraint('disclosure_request_id', 'field_key', name='ux_disc_req_field'),
    )

class DisclosureRequestEvent(Base):
    __tablename__ = 'disclosure_request_events'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    disclosure_request_id = Column(UUID(as_uuid=True), ForeignKey('disclosure_requests.id'), nullable=False)
    from_status = Column(String) # Enum DisclosureStatus
    to_status = Column(String, nullable=False) # Enum DisclosureStatus
    actor_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    actor_kind = Column(String, nullable=False) # Enum ActorKind
    detail = Column(JSONB, nullable=False, server_default='{}')
    occurred_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class VaspResponse(Base):
    __tablename__ = 'vasp_responses'
    id = Column(UUID(as_uuid=True), primary_key=True)
    disclosure_request_id = Column(UUID(as_uuid=True), ForeignKey('disclosure_requests.id'), nullable=False)
    received_at = Column(DateTime(timezone=True), nullable=False)
    response_kind = Column(Text, nullable=False)
    rejection_reason = Column(Text)
    address_confirmed_ours = Column(Boolean)
    attachment_object_key = Column(Text)
    attachment_sha256 = Column(LargeBinary)
    recorded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

# ==========================================
# 15. MODEL REGISTRY & MLOPS
# ==========================================

class ModelFamily(Base):
    __tablename__ = 'model_families'
    id = Column(SmallInteger, primary_key=True)
    family_key = Column(Text, nullable=False, unique=True)
    display_name = Column(Text, nullable=False)
    task = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

class ModelVersion(Base):
    __tablename__ = 'model_versions'
    id = Column(UUID(as_uuid=True), primary_key=True)
    family_id = Column(SmallInteger, ForeignKey('model_families.id'), nullable=False)
    semver = Column(Text, nullable=False)
    artifact_object_key = Column(Text, nullable=False)
    artifact_sha256 = Column(LargeBinary, nullable=False)
    framework = Column(Text, nullable=False)
    stage = Column(String, nullable=False, default=ModelStage.TRAINING.value)
    
    training_dataset_ref = Column(Text, nullable=False)
    split_strategy = Column(Text, nullable=False)
    train_window_end = Column(DateTime(timezone=True))
    class_balance = Column(JSONB, nullable=False)
    hyperparameters = Column(JSONB, nullable=False)
    feature_set_version = Column(Text, nullable=False)
    synthetic_data_fraction = Column(Numeric(5,4), nullable=False, default=0)
    
    model_card_object_key = Column(Text)
    known_failure_modes = Column(Text)
    prohibited_uses = Column(Text)
    
    trained_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    trained_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('family_id', 'semver', name='ux_model_family_semver'),
        CheckConstraint("""split_strategy = 'TEMPORAL'""", name='ck_model_split'),
        CheckConstraint(
            """stage NOT IN ('ACTIVE','SHADOW') OR (model_card_object_key IS NOT NULL AND known_failure_modes IS NOT NULL AND prohibited_uses IS NOT NULL)""",
            name='ck_model_promo_requires_card'
        ),
    )

class ModelEvaluation(Base):
    __tablename__ = 'model_evaluations'
    id = Column(UUID(as_uuid=True), primary_key=True)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey('model_versions.id'), nullable=False)
    dataset_ref = Column(Text, nullable=False)
    split_name = Column(Text, nullable=False)
    
    precision_minority = Column(Numeric(6,5))
    recall_minority = Column(Numeric(6,5))
    f1_minority = Column(Numeric(6,5))
    pr_auc = Column(Numeric(6,5))
    roc_auc = Column(Numeric(6,5))
    confusion_matrix = Column(JSONB)
    
    expected_calib_error = Column(Numeric(6,5))
    brier_score = Column(Numeric(6,5))
    reliability_curve = Column(JSONB)
    
    bootstrap_ci = Column(JSONB)
    stratified_by_decile = Column(JSONB)
    ablation_results = Column(JSONB)
    baseline_comparison = Column(JSONB)
    negative_findings = Column(Text)
    
    evaluated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    evaluated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))

class ModelPromotion(Base):
    __tablename__ = 'model_promotions'
    id = Column(UUID(as_uuid=True), primary_key=True)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey('model_versions.id'), nullable=False)
    from_stage = Column(String, nullable=False) # Enum ModelStage
    to_stage = Column(String, nullable=False) # Enum ModelStage
    proposed_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    justification = Column(Text, nullable=False)
    shadow_window_start = Column(DateTime(timezone=True))
    shadow_window_end = Column(DateTime(timezone=True))
    promoted_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint('proposed_by <> approved_by', name='ck_promo_two_person'),
    )

class ModelDriftObservation(Base):
    __tablename__ = 'model_drift_observations'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey('model_versions.id'), nullable=False)
    window_start = Column(DateTime(timezone=True), nullable=False)
    window_end = Column(DateTime(timezone=True), nullable=False)
    abstention_rate = Column(Numeric(6,5))
    mean_max_probability = Column(Numeric(6,5))
    feature_psi = Column(JSONB)
    override_rate = Column(Numeric(6,5))
    alert_raised = Column(Boolean, nullable=False, default=False)

# ==========================================
# 16. IMMUTABLE AUDIT LOG
# ==========================================

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    occurred_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    actor_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    actor_kind = Column(String, nullable=False) # Enum ActorKind
    actor_session_id = Column(UUID(as_uuid=True))
    source_ip = Column(INET)
    
    action = Column(Text, nullable=False)
    entity_type = Column(Text, nullable=False)
    entity_id = Column(UUID(as_uuid=True))
    case_id = Column(UUID(as_uuid=True))
    severity = Column(String, nullable=False, default=AuditSeverity.INFO.value)
    
    before_state = Column(JSONB)
    after_state = Column(JSONB)
    payload_digest = Column(LargeBinary, nullable=False)
    
    prev_entry_hash = Column(LargeBinary)
    entry_hash = Column(LargeBinary, nullable=False)
    
    __table_args__ = (
        CheckConstraint('octet_length(entry_hash) = 32', name='ck_audit_hash_len'),
    )

class AuditChainCheckpoint(Base):
    __tablename__ = 'audit_chain_checkpoints'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    checked_through_id = Column(BigInteger, nullable=False)
    chain_head_hash = Column(LargeBinary, nullable=False)
    is_intact = Column(Boolean, nullable=False)
    broken_at_id = Column(BigInteger)
    checked_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    external_anchor_ref = Column(Text)

