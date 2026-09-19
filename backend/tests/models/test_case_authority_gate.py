import pytest
from sqlalchemy import CheckConstraint
from app.models.canonical import Case

def test_case_authority_gate_constraint_exists():
    # Verify the CheckConstraint for lawful authority gate exists in AST/reflection
    constraints = [c for c in Case.__table__.constraints if isinstance(c, CheckConstraint)]
    
    authority_constraint = next((c for c in constraints if c.name == 'ck_case_authority_present'), None)
    
    assert authority_constraint is not None, "Lawful authority gate CheckConstraint missing"
    
    # Verify the SQL logic matches spec
    sql_text = str(authority_constraint.sqltext)
    assert "status = 'DRAFT'" in sql_text
    assert "fir_number IS NOT NULL" in sql_text
    assert "ncrp_acknowledgement IS NOT NULL" in sql_text
    assert "written_authority_ref IS NOT NULL" in sql_text
