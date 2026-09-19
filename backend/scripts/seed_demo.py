import sys
import os
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from app.core.config import settings

def seed_demo_data():
    # Use standard sync driver for quick insert
    url = settings.DATABASE_URL.replace("+psycopg", "")
    engine = create_engine(url)
    
    statements = [
        "INSERT INTO cases (id, fir_number, io_designation, authority_ref, status) VALUES ('CASE-DEMO', 'DL-CYBER-2025-001', 'Inspector Demo', 'SEC94-BNSS-DEMO', 'OPEN');",
        "INSERT INTO case_seed_addresses (id, case_id, address, chain) VALUES ('SEED-1', 'CASE-DEMO', '1A1zP1eP5QGefi2DMPTfTL5SLmv7Divf', 'bitcoin');",
        "INSERT INTO case_seed_addresses (id, case_id, address, chain) VALUES ('SEED-2', 'CASE-DEMO', '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045', 'ethereum');",
        "INSERT INTO vasp_entities (id, name, is_fiu_registered) VALUES ('VASP-DEMO', 'DemoExchange', true);",
        "INSERT INTO traces (id, case_id, seed_address, status) VALUES ('TRACE-DEMO', 'CASE-DEMO', '1A1zP1eP5QGefi2DMPTfTL5SLmv7Divf', 'COMPLETED');",
        "INSERT INTO confidence_scores (id, trace_id, score, requires_review) VALUES ('CONF-1', 'TRACE-DEMO', 0.87, false);"
    ]
    
    with engine.begin() as conn:
        for stmt in statements:
            try:
                conn.execute(text(stmt))
            except Exception as e:
                logging.warning(f"Ignoring duplicate or schema insert error: {e}")
                
    print("Demo fixture data seeded successfully.")

if __name__ == "__main__":
    seed_demo_data()
