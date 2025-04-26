from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Body,
    File,
    UploadFile,
    Form,
    Depends,
)
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import uuid
from datetime import date, datetime
import io
import os
import tempfile
import shutil
import PyPDF2
from app.clients.extract_case_type import extract_case_type
from app.clients.extract_other_types import extract_other_types

from app.db.database import (
    get_case_summaries,
    get_case_by_id,
    add_new_case,
)
from app.models.models import Case, CaseSummary, CreateCaseRequest, CaseResponse

router = APIRouter(
    prefix="/cases",
    tags=["cases"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CaseSummary])
async def get_cases(
    search: Optional[str] = Query(
        None, description="Search query for case title or jurisdiction"
    )
):
    """
    Get all cases, with optional search filtering
    """
    cases = get_case_summaries()

    if search:
        search = search.lower()
        return [
            case
            for case in cases
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


@router.post("/", response_model=CaseResponse)
async def create_case(files: List[UploadFile] = File(None)):
    """
    Create a new case with uploaded documents.
    The backend will extract text from PDFs and create a new case.
    """
    # Generate a unique ID for the new case
    case_id = str(uuid.uuid4())[:8]

    # Set default values for a new case
    extracted_text = ""

    # Function to extract text from files using PyPDF2 for PDFs
    def extract_text_from_file(file_content: bytes, filename: str) -> str:
        """Extract text from files, supporting PDF and text files."""
        extracted_text = ""

        try:
            if filename.lower().endswith(".pdf"):
                # For PDF files, use PyPDF2
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    extracted_text += page.extract_text() + "\n"
            elif filename.lower().endswith((".txt", ".md", ".rtf")):
                # For text files, decode the content
                extracted_text = file_content.decode("utf-8", errors="ignore")
            else:
                # For unsupported file types
                extracted_text = f"[Content extraction not supported for {filename}]"
        except Exception as e:
            extracted_text = f"[Error extracting text from {filename}: {str(e)}]"

        return extracted_text

    # Process uploaded files
    if files:
        for file in files:
            try:
                # Read file content
                contents = await file.read()

                # Extract text from file
                file_text = extract_text_from_file(contents, file.filename)
                extracted_text += f"--- From {file.filename} ---\n{file_text}\n\n"

                # Reset file position for potential future reads
                await file.seek(0)
            except Exception as e:
                print(f"Error processing file {file.filename}: {str(e)}")

    print(extracted_text)

    
    extract_case_type_response = extract_case_type(extracted_text)
    extract_other_types_response = extract_other_types(extracted_text)


    print(extract_case_type_response)
    print(extract_other_types_response)


    print("Extracted Case Type Response:")


    # Parse the data from extract_case_type_response
    case_type = extract_case_type_response.primary_analysis.case_type
    harm_type = extract_case_type_response.primary_analysis.harm_type
    cause = extract_case_type_response.primary_analysis.cause
    description = extract_case_type_response.primary_analysis.description
    secondary_types = extract_case_type_response.primary_analysis.secondary_types or []


    # Parse possible alternatives from extract_case_type_response
    possible_alternatives = extract_case_type_response.possible_alternatives or []


    # Parse the data from extract_other_types_response
    case_id = extract_other_types_response.Case_ID
    filing_date = extract_other_types_response.Filing_Date
    jurisdiction = extract_other_types_response.Jurisdiction
    defect_type = extract_other_types_response.Defect_Type or []
    number_of_claimants = extract_other_types_response.Number_of_Claimants
    media_coverage_level = extract_other_types_response.Media_Coverage_Level
    outcome = extract_other_types_response.Outcome
    time_to_resolution_months = extract_other_types_response.Time_to_Resolution_Months
    settlement_amount = extract_other_types_response.Settlement_Amount
    defense_cost_estimate = extract_other_types_response.Defense_Cost_Estimate
    expected_brand_impact = extract_other_types_response.Expected_Brand_Impact

    # Parse the new information from extract_other_types_response
    affected_car = extract_other_types_response.Affected_Car
    affected_part = extract_other_types_response.Affected_Part
    brand_impact_estimate = extract_other_types_response.Brand_Impact_Estimate
    case_win_likelihood = extract_other_types_response.Case_Win_Likelihood
    plaintiff_argumentation = extract_other_types_response.Plaintiff_Argumentation or []

    # Print parsed variables for debugging (optional)
    print("Parsed Case Type Response:")
    print(f"Case Type: {case_type}")
    print(f"Harm Type: {harm_type}")
    print(f"Cause: {cause}")
    print(f"Description: {description}")
    print(f"Secondary Types: {secondary_types}")
    print(f"Possible Alternatives: {possible_alternatives}")


    print("\nParsed Other Types Response:")
    print(f"Case ID: {case_id}")
    print(f"Filing Date: {filing_date}")
    print(f"Jurisdiction: {jurisdiction}")
    print(f"Defect Type: {defect_type}")
    print(f"Number of Claimants: {number_of_claimants}")
    print(f"Media Coverage Level: {media_coverage_level}")
    print(f"Outcome: {outcome}")
    print(f"Time to Resolution (Months): {time_to_resolution_months}")
    print(f"Settlement Amount: {settlement_amount}")
    print(f"Defense Cost Estimate: {defense_cost_estimate}")
    print(f"Expected Brand Impact: {expected_brand_impact}")

    # Print the new information
    print("\nNew Information:")
    print(f"Affected Car: {affected_car}")
    print(f"Affected Part: {affected_part}")
    print(f"Brand Impact Estimate: {brand_impact_estimate}")
    print(f"Case Win Likelihood: {case_win_likelihood}")
    print(f"Plaintiff Argumentation: {plaintiff_argumentation}")


    # Generate case metadata from extracted text
    today = datetime.now().strftime("%Y-%m-%d")

    # Mock extraction of title from text
    title = "New Case"
    if "Bayerische vs" in extracted_text:
        title = "Bayerische vs. Johnson"
    elif "v." in extracted_text:
        # Look for patterns like "Smith v. Jones"
        import re

        match = re.search(r"([A-Za-z\s]+)\s+v\.\s+([A-Za-z\s]+)", extracted_text)
        if match:
            title = match.group(0)

    # Create a new case object
    new_case = {
        "id": case_id,
        "title": case_id,
        "status": "in progress",
        "jurisdiction": jurisdiction,  # Mock jurisdiction
        "caseType": case_type,  # Mock case type
        "date": filing_date,
        "relevantLaws": [],
        "timeline": [{
            "date": today,
            "event": "Case created",
            "description": "Initial case documents uploaded"
        }],
        "offenseArgumentation": plaintiff_argumentation,
        "timeline": [
            {
                "date": today,
                "event": "Case created",
                "description": "Initial case documents uploaded",
            }
        ],
        "offenseArgumentation": extracted_text,
        "defenseArgumentation": None,
        "suggestions": [],
        "outcomePrediction": None,
        # Add the additional extracted information
        "defectType": defect_type,
        "numberOfClaimants": number_of_claimants,
        "mediaCoverageLevel": media_coverage_level,
        "outcome": outcome,
        "timeToResolutionMonths": time_to_resolution_months,
        "settlementAmount": settlement_amount,
        "defenseCostEstimate": defense_cost_estimate,
        "expectedBrandImpact": expected_brand_impact,
    }

    # Add the case to the database
    success = add_new_case(case_id, new_case)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to create case")

    # Return the ID of the newly created case
    return {"id": case_id}
