from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.db.database import (
    get_case_summaries,
    get_case_by_id,
)
from app.models.models import Case, CaseSummary

router = APIRouter(
    prefix="/cases",
    tags=["cases"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[CaseSummary])
async def get_cases(
    search: Optional[str] = Query(None, description="Search query for case title or jurisdiction")
):
    """
    Get all cases, with optional search filtering
    """
    cases = get_case_summaries()
    
    if search:
        search = search.lower()
        return [
            case for case in cases
            if search in case["title"].lower() or search in case["jurisdiction"].lower()
        ]
    return cases

@router.get("/{case_id}", response_model=Case)
async def get_case(case_id: str):
    """
    Get detailed information for a specific case
    """
    case = get_case_by_id(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case