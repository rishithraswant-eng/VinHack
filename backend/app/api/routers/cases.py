from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class CaseResponse(BaseModel):
    case_id: str
    authority: str
    seed_address: str
    fir_number: str = ""
    io_designation: str = ""

class CaseCreateRequest(BaseModel):
    case_id: str
    authority: str
    seed_address: str
    fir_number: str = ""
    io_designation: str = ""

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
    return CASES_DB[case_data.case_id]
