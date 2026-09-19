"""
Exports OpenAPI JSON contract for frontend client generation.
Implements T1.PLT.04.
"""

import json
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.main import app


def export_schema(output_path: Path):
    openapi_schema = app.openapi()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"Exported OpenAPI schema to: {output_path}")

if __name__ == "__main__":
    target = backend_dir / "openapi.json"
    export_schema(target)
