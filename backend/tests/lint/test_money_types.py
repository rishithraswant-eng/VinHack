"""
Engineering Standard ES-01 CI Lint:
"Money is NUMERIC(78,0) base units. A CI lint rejects FLOAT/REAL/DOUBLE columns matching /(value|amount|balance|fee)/."
"""

import re

from sqlalchemy import REAL, Column, Float, Integer, Numeric, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import Double

MONEY_COLUMN_PATTERN = re.compile(r"(value|amount|balance|fee)", re.IGNORECASE)
FORBIDDEN_TYPES = (Float, REAL, Double)


def check_column_es01_compliance(column_name: str, column_type) -> list[str]:
    """
    Checks if a column violates ES-01:
    - If the column name matches /(value|amount|balance|fee)/:
      It must NOT be Float, REAL, or Double.
      It should be Numeric(78, 0) base units or integer units.
    Returns a list of violation messages.
    """
    violations = []
    if MONEY_COLUMN_PATTERN.search(column_name):
        # Check forbidden float types
        if isinstance(column_type, FORBIDDEN_TYPES):
            violations.append(
                f"Column '{column_name}' violates ES-01: type {column_type.__class__.__name__} "
                f"is forbidden for monetary columns matching /(value|amount|balance|fee)/. "
                f"Must use NUMERIC(78, 0) base units."
            )
        elif isinstance(column_type, Numeric) and (
            column_type.precision != 78 or column_type.scale != 0
        ):
            violations.append(
                f"Column '{column_name}' violates ES-01: Numeric precision={column_type.precision}, "
                f"scale={column_type.scale}. Expected NUMERIC(78, 0) for uint256 base units."
            )
    return violations


def validate_model_class(model_cls) -> list[str]:
    """Inspect all columns of a SQLAlchemy model class for ES-01 compliance."""
    violations = []
    if hasattr(model_cls, "__table__") and isinstance(model_cls.__table__, Table):
        for col in model_cls.__table__.columns:
            violations.extend(check_column_es01_compliance(col.name, col.type))
    return violations


# ---------------------------------------------------------------------------
# Unit tests for the ES-01 linter itself
# ---------------------------------------------------------------------------

LintTestBase = declarative_base()


class InvalidFloatModel(LintTestBase):
    __tablename__ = "test_invalid_float"
    id = Column(Integer, primary_key=True)
    transfer_amount = Column(Float, nullable=False)


class InvalidRealModel(LintTestBase):
    __tablename__ = "test_invalid_real"
    id = Column(Integer, primary_key=True)
    fee_paid = Column(REAL, nullable=False)


class InvalidNumericScaleModel(LintTestBase):
    __tablename__ = "test_invalid_scale"
    id = Column(Integer, primary_key=True)
    balance_amount = Column(Numeric(18, 8), nullable=False)


class ValidMoneyModel(LintTestBase):
    __tablename__ = "test_valid_money"
    id = Column(Integer, primary_key=True)
    amount_base_units = Column(Numeric(78, 0), nullable=False)
    fee_base_units = Column(Numeric(78, 0), nullable=False)
    unrelated_float = Column(Float, nullable=True)  # Name does not match money regex


def test_es01_linter_detects_float_violations():
    """Verify that Float column matching money pattern is caught and reported."""
    violations = validate_model_class(InvalidFloatModel)
    assert len(violations) == 1
    assert "transfer_amount" in violations[0]
    assert "Float is forbidden" in violations[0]


def test_es01_linter_detects_real_violations():
    """Verify that REAL column matching fee pattern is caught and reported."""
    violations = validate_model_class(InvalidRealModel)
    assert len(violations) == 1
    assert "fee_paid" in violations[0]
    assert "REAL is forbidden" in violations[0]


def test_es01_linter_detects_non_78_scale_violations():
    """Verify that Numeric without (78, 0) is caught and reported."""
    violations = validate_model_class(InvalidNumericScaleModel)
    assert len(violations) == 1
    assert "balance_amount" in violations[0]
    assert "Expected NUMERIC(78, 0)" in violations[0]


def test_es01_linter_passes_valid_model():
    """Verify that models with NUMERIC(78, 0) pass without violations."""
    violations = validate_model_class(ValidMoneyModel)
    assert violations == []


def test_es01_all_registered_models():
    """
    Scans all registered SQLAlchemy models in the application.
    If models exist, ensures zero ES-01 violations.
    """
    try:
        from app.db.base import Base
        all_violations = []
        for mapper in Base.registry.mappers:
            all_violations.extend(validate_model_class(mapper.class_))
        assert all_violations == [], f"ES-01 violations found in application models: {all_violations}"
    except ImportError:
        # Base will be imported in Component 2 when canonical.py is created
        pass
