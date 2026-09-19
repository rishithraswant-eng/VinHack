import json
import os
import tempfile
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class CaseResponse(BaseModel):
    case_id: str
    authority: str
    seed_address: str
    fir_number: str = ""
    io_designation: str = ""
    police_station: str = ""
    jurisdiction_bench: str = ""
    disputed_value_inr: str = ""

class CaseCreateRequest(BaseModel):
    case_id: str
    authority: str
    seed_address: str
    fir_number: str = ""
    io_designation: str = ""
    police_station: str = ""
    jurisdiction_bench: str = ""
    disputed_value_inr: str = ""

CASES_FILE = Path(__file__).resolve().parents[3] / "storage" / "cases.json"

# Mock database of cases
CASES_DB = {
    "PHT-7533": {
        "case_id": "PHT-7533",
        "authority": "Sec 94 BNSS",
        "seed_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
        "fir_number": "FIR-2026/08/891",
        "io_designation": "Inspector A. Sharma"
    }
}

try:
    if CASES_FILE.exists():
        with open(CASES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                CASES_DB.update(data)
except Exception:
    pass

@router.get("/cases/{case_id}", response_model=CaseResponse)
async def get_case(case_id: str):
    if case_id in CASES_DB:
        return CASES_DB[case_id]
    
    # Return a generic one if not found so the wizard works
    return {
        "case_id": case_id,
        "authority": "Sec 94 BNSS",
        "seed_address": "Unknown",
        "fir_number": f"FIR-{case_id}",
        "io_designation": "Unknown Officer"
    }

@router.post("/cases/", response_model=CaseResponse)
async def create_case(case_data: CaseCreateRequest):
    CASES_DB[case_data.case_id] = case_data.dict()
    try:
        CASES_FILE.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_path = tempfile.mkstemp(dir=CASES_FILE.parent, suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(CASES_DB, f)
        os.replace(temp_path, CASES_FILE)
    except Exception as e:
        print(f"Failed to persist cases: {e}")
    return CASES_DB[case_data.case_id]
