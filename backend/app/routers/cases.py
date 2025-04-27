from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    File,
    UploadFile,
)
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import uuid
from datetime import date, datetime
import io
import PyPDF2
from app.clients.extract_case_type import extract_case_type
from app.clients.extract_other_types import extract_other_types
from app.clients.prediction import add_win_likelihood_to_case

from app.db.database import (
    get_case_summaries,
    get_case_by_id,
    add_new_case,
)
from app.clients.embed import embed, find_similar
from app.models.models import Case, CaseResponse

router = APIRouter(
    prefix="/cases",
    tags=["cases"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
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


@router.get("/{case_id}")
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

    # Extract evidence from the primary analysis
    evidence = extract_case_type_response.primary_analysis.evidence or []

    # Parse possible alternatives from extract_case_type_response
    possible_alternatives = extract_case_type_response.possible_alternatives or []

    # Extract evidence from possible alternatives if available
    for alt in possible_alternatives:
        if hasattr(alt, "evidence") and alt.evidence:
            # Add evidence from alternatives to a separate field if needed
            alt_evidence = alt.evidence
        else:
            alt_evidence = []

    # Parse the data from extract_other_types_response
    case_id_from_extract = extract_other_types_response.Case_ID
    filing_date_raw = extract_other_types_response.Filing_Date
    try:
        # Try to parse the date assuming the format "YYYY-MM-DD"
        filing_date_obj = datetime.strptime(filing_date_raw, "%Y-%m-%d")
        filing_date = filing_date_obj.strftime("%Y-%m-%d")
    except Exception:
        filing_date = "Not specified"

    # Handle the new jurisdiction format (now a dictionary)
    jurisdiction = extract_other_types_response.Jurisdiction
    state_jurisdiction = (
        jurisdiction.get("state_jurisdiction", "Not specified")
        if isinstance(jurisdiction, dict)
        else "Not specified"
    )
    court_jurisdiction = (
        jurisdiction.get("court_jurisdiction", "Not specified")
        if isinstance(jurisdiction, dict)
        else jurisdiction
    )

    defect_type = extract_other_types_response.Defect_Type or []
    number_of_claimants = str(extract_other_types_response.Number_of_Claimants)
    media_coverage_level = extract_other_types_response.Media_Coverage_Level
    outcome = extract_other_types_response.Outcome

    # Convert status to match the expected values from the new valid statuses
    status_raw = extract_other_types_response.Status
    valid_statuses = [
        "In favour of defendant",
        "In favour of plaintiff",
        "Settled",
        "In Progress first instance",
        "Dismissed",
        "In Progress appeal",
        "In Progress Supreme Court",
    ]

    if isinstance(status_raw, str) and status_raw in valid_statuses:
        status = status_raw
    elif isinstance(status_raw, str) and status_raw == "Not specified":
        status = "In Progress first instance"  # Default value
    else:
        status = "In Progress first instance"  # Default value

    case_summary = extract_other_types_response.Case_Summary
    time_to_resolution_months = extract_other_types_response.Time_to_Resolution_Months
    settlement_amount = extract_other_types_response.Settlement_Amount
    defense_cost_estimate = extract_other_types_response.Defense_Cost_Estimate
    expected_brand_impact = extract_other_types_response.Expected_Brand_Impact

    # Parse the new and updated information from extract_other_types_response
    affected_car = extract_other_types_response.Affected_Car
    affected_part = extract_other_types_response.Affected_Part
    brand_impact_estimate = extract_other_types_response.Brand_Impact_Estimate
    case_win_likelihood = extract_other_types_response.Case_Win_Likelihood

    # Get plaintiff argumentation as a list of key points
    plaintiff_argumentation = extract_other_types_response.Plaintiff_Argumentation or []

    # Get the new fields
    timeline_of_events = extract_other_types_response.Timeline_of_Events or []
    relevant_laws = extract_other_types_response.Relevant_Laws or []

    # Get the separated reputation impact
    reputation_impact = extract_other_types_response.Reputation_Impact or {
        "case_outcome": {
            "impact": "Not specified",
            "explanation": "Insufficient information to determine",
        },
        "media_coverage": {
            "impact": "Not specified",
            "explanation": "Insufficient information to determine",
        },
    }

    reputation_impact_case = reputation_impact.get("case_outcome", {})
    reputation_impact_media = reputation_impact.get("media_coverage", {})

    # Print parsed variables for debugging (optional)
    print("Parsed Case Type Response:")
    print(f"Case Type: {case_type}")
    print(f"Harm Type: {harm_type}")
    print(f"Cause: {cause}")
    print(f"Description: {description}")
    print(f"Secondary Types: {secondary_types}")
    print(f"Evidence: {evidence}")
    print(f"Possible Alternatives: {possible_alternatives}")

    print("\nParsed Other Types Response:")
    print(f"Case ID: {case_id_from_extract}")
    print(f"Filing Date: {filing_date}")
    print(f"State Jurisdiction: {state_jurisdiction}")
    print(f"Court Jurisdiction: {court_jurisdiction}")
    print(f"Defect Type: {defect_type}")
    print(f"Number of Claimants: {number_of_claimants}")
    print(f"Media Coverage Level: {media_coverage_level}")
    print(f"Outcome: {outcome}")
    print(f"Status: {status}")
    print(f"Case Summary: {case_summary}")
    print(f"Time to Resolution (Months): {time_to_resolution_months}")
    print(f"Settlement Amount: {settlement_amount}")
    print(f"Defense Cost Estimate: {defense_cost_estimate}")
    print(f"Expected Brand Impact: {expected_brand_impact}")

    # Print the new and updated information
    print("\nNew and Updated Information:")
    print(f"Affected Car: {affected_car}")
    print(f"Affected Part: {affected_part}")
    print(f"Brand Impact Estimate: {brand_impact_estimate}")
    print(f"Case Win Likelihood: {case_win_likelihood}")
    print(f"Plaintiff Argumentation: {plaintiff_argumentation}")
    print(f"Timeline of Events: {timeline_of_events}")
    print(f"Relevant Laws: {relevant_laws}")
    print(f"Reputation Impact (Case Outcome): {reputation_impact_case}")
    print(f"Reputation Impact (Media Coverage): {reputation_impact_media}")

    # Generate case metadata from extracted text
    today = datetime.now().strftime("%Y-%m-%d")

    # Function to extract date from timeline event string
    def extract_date_from_event(event_str):
        """
        Extract date from event string using various patterns.
        Returns the date in YYYY-MM-DD format if found, otherwise None.
        """
        import re
        from datetime import datetime

        # Common date patterns
        patterns = [
            # YYYY-MM-DD
            r"(\d{4}-\d{1,2}-\d{1,2})",
            # MM/DD/YYYY
            r"(\d{1,2}/\d{1,2}/\d{4})",
            # Month DD, YYYY
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}",
            # DD Month YYYY
            r"(\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})",
            # Month YYYY
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
        ]

        for pattern in patterns:
            match = re.search(pattern, event_str)
            if match:
                date_str = match.group(0)
                try:
                    # Try various date formats
                    for fmt in (
                        "%Y-%m-%d",
                        "%m/%d/%Y",
                        "%B %d, %Y",
                        "%d %B %Y",
                        "%B %Y",
                    ):
                        try:
                            date_obj = datetime.strptime(date_str, fmt)
                            # If only month and year, set day to 1
                            if fmt == "%B %Y":
                                return date_obj.strftime("%Y-%m-01")
                            return date_obj.strftime("%Y-%m-%d")
                        except ValueError:
                            continue
                except Exception:
                    pass

        # If no date pattern found or parsing failed
        return None

    # Process timeline events to extract dates
    processed_timeline = []

    # Process the extracted timeline events
    for event in timeline_of_events:
        if event != "Not specified":
            # Try to extract a date from the event text
            event_date = extract_date_from_event(event)

            # If filing_date is available and no date found in the event,
            # use filing_date for events that seem to be about the filing
            if not event_date and filing_date and filing_date != "Not specified":
                if any(
                    filing_term in event.lower()
                    for filing_term in [
                        "filed",
                        "filing",
                        "complaint",
                        "initiated",
                        "commenced",
                    ]
                ):
                    event_date = filing_date

            # Add the event to the timeline with the extracted date or "Unknown"
            processed_timeline.append(
                {
                    "date": event_date if event_date else "Unknown",
                    "event": event,
                    "description": "",
                }
            )

    # Process evidence for storage in the database
    processed_evidence = []
    if evidence:
        for item in evidence:
            processed_evidence.append(
                {
                    "text": (
                        item.text if hasattr(item, "text") else item.get("text", "")
                    ),
                    "relevance": (
                        item.relevance
                        if hasattr(item, "relevance")
                        else item.get("relevance", "")
                    ),
                    "strength": (
                        item.strength
                        if hasattr(item, "strength")
                        else item.get("strength", "")
                    ),
                }
            )

    # Create a new case object with updated field names
    new_case = {
        "id": case_id,
        "title": case_id,
        "status": status,
        "jurisdiction": f"{state_jurisdiction} - {court_jurisdiction}",  # Keep the jurisdiction field for backward compatibility
        "stateJurisdiction": state_jurisdiction,
        "courtJurisdiction": court_jurisdiction,
        "caseType": case_type,
        "harmType": harm_type,
        "cause": cause,
        "description": description,
        "secondaryTypes": secondary_types,
        "possibleAlternatives": possible_alternatives,
        "evidence": processed_evidence,  # Add the evidence to the case
        "date": filing_date,
        "relevantLaws": relevant_laws if relevant_laws != ["Not specified"] else [],
        "timeline": processed_timeline,
        "plaintiffArgumentation": (
            plaintiff_argumentation
            if plaintiff_argumentation != ["Not specified"]
            else []
        ),
        "defenseArgumentation": "",
        "suggestions": [],
        "numberOfClaimants": number_of_claimants,
        "mediaCoverageLevel": media_coverage_level,
        "outcome": outcome,
        "caseSummary": case_summary,
        "timeToResolutionMonths": time_to_resolution_months,
        "settlementAmount": settlement_amount,
        "defenseCostEstimate": defense_cost_estimate,
        "expectedBrandImpact": expected_brand_impact,
        "affectedCar": affected_car,
        "affectedPart": affected_part,
        "brandImpactEstimate": brand_impact_estimate,
        "caseWinLikelihood": case_win_likelihood,
        "reputationImpactCase": reputation_impact_case,
        "reputationImpactMedia": reputation_impact_media,
    }

    new_case = embed(new_case)
    new_case = find_similar(new_case, threshold=0.5, top_k=5)

    new_case = add_win_likelihood_to_case(new_case)

    # Add the case to the database
    success = add_new_case(case_id, new_case)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to create case")

    # Return the ID of the newly created case
    return {"id": case_id}
