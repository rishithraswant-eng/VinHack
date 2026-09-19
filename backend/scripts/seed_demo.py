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
        # Removed hardcoded fake demo data per requirements
        # System now operates dynamically
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
