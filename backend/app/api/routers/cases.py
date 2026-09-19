from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class CaseResponse(BaseModel):
    case_id: str
    authority: str
    seed_address: str

# Mock database of cases
CASES_DB = {
    "PHT-7533": {
        "case_id": "PHT-7533",
        "authority": "Sec 94 BNSS (FIR-2026/08/891)",
        "seed_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    }
}

@router.get("/cases/{case_id}", response_model=CaseResponse)
async def get_case(case_id: str):
    if case_id in CASES_DB:
        return CASES_DB[case_id]
    
    # Return a generic one if not found so the wizard works
    return {
        "case_id": case_id,
        "authority": "Sec 94 BNSS (FIR-Generic)",
        "seed_address": "Unknown"
    }
