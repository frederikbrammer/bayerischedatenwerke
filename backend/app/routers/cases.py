from fastapi import APIRouter, HTTPException, Query, Body, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import uuid
from datetime import date, datetime
import io
import os
import tempfile
import shutil
import PyPDF2

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

@router.post("/", response_model=CaseResponse)
async def create_case(
    files: List[UploadFile] = File(None)
):
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
            if filename.lower().endswith('.pdf'):
                # For PDF files, use PyPDF2
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    extracted_text += page.extract_text() + "\n"
            elif filename.lower().endswith(('.txt', '.md', '.rtf')):
                # For text files, decode the content
                extracted_text = file_content.decode('utf-8', errors='ignore')
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
    
    # Generate case metadata from extracted text
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Mock extraction of title from text
    title = "New Case"
    if "Bayerische vs" in extracted_text:
        title = "Bayerische vs. Johnson"
    elif "v." in extracted_text:
        # Look for patterns like "Smith v. Jones"
        import re
        match = re.search(r'([A-Za-z\s]+)\s+v\.\s+([A-Za-z\s]+)', extracted_text)
        if match:
            title = match.group(0)
    
    # Create a new case object
    new_case = {
        "id": case_id,
        "title": title,
        "status": "in progress",
        "jurisdiction": "California",  # Mock jurisdiction
        "caseType": "Liability",       # Mock case type
        "date": today,
        "relevantLaws": [],
        "timeline": [{
            "date": today,
            "event": "Case created",
            "description": "Initial case documents uploaded"
        }],
        "offenseArgumentation": extracted_text,
        "defenseArgumentation": None,
        "suggestions": [],
        "outcomePrediction": None
    }
    
    # Add the case to the database
    success = add_new_case(case_id, new_case)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create case")
    
    # Return the ID of the newly created case
    return {"id": case_id}