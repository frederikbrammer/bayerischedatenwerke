import json
import os
from typing import Dict, List, Optional
from app.models.models import Case, CaseSummary

# Paths
DB_DIR = os.path.dirname(os.path.abspath(__file__))
CASES_DB_PATH = os.path.join(DB_DIR, "cases.json")

# Sample case data for database
SAMPLE_CASE_DATA = {
    "1": {
        "id": "1",
        "title": "Smith v. Bayersche Motors",
        "status": "won",
        "jurisdiction": "California",
        "caseType": "Liability",
        "date": "2023-05-15",
        "relevantLaws": [
            "California Vehicle Code § 27315",
            "California Civil Code § 1793.2",
        ],
        "timeline": [
            {
                "date": "2023-01-10",
                "event": "Initial complaint filed",
                "description": "Plaintiff filed complaint alleging faulty braking system",
            },
            {
                "date": "2023-02-15",
                "event": "Response filed",
                "description": "Bayersche Motors filed response denying allegations",
            },
            {
                "date": "2023-03-20",
                "event": "Discovery phase",
                "description": "Exchange of documents and expert testimonies",
            },
            {
                "date": "2023-04-25",
                "event": "Court hearing",
                "description": "Judge ruled in favor of Bayersche Motors",
            },
            {
                "date": "2023-05-15",
                "event": "Case closed",
                "description": "Case officially closed with favorable outcome",
            },
        ],
        "offenseArgumentation": "The plaintiff claimed that the braking system in the Model S was defective, causing a collision. They argued that Bayersche Motors was aware of the defect but failed to issue a recall or properly warn customers.",
        "defenseArgumentation": "Our defense demonstrated that the braking system met all safety standards and that the collision was caused by driver error rather than any defect in the vehicle. Expert testimony confirmed the braking system functioned as designed.",
        "suggestions": [
            "Reference the Johnson v. AutoCorp case where similar claims were dismissed",
            "Include more technical data from the vehicle's diagnostic system",
            "Emphasize driver training requirements in the owner's manual",
        ],
        "outcomePrediction": {
            "cost": "$150,000 - $250,000",
            "reputationalLoss": "Low",
            "winProbability": "85%",
        },
    },
    "2": {
        "id": "2",
        "title": "Johnson Family Trust v. Bayersche",
        "status": "lost",
        "jurisdiction": "New York",
        "caseType": "Liability",
        "date": "2023-08-22",
        "relevantLaws": [
            "New York Vehicle and Traffic Law § 375",
            "New York General Business Law § 349",
        ],
        "timeline": [
            {
                "date": "2023-03-05",
                "event": "Initial complaint filed",
                "description": "Plaintiff alleged engine defect causing fire hazard",
            },
            {
                "date": "2023-04-12",
                "event": "Response filed",
                "description": "Bayersche filed response contesting allegations",
            },
            {
                "date": "2023-05-20",
                "event": "Expert testimony",
                "description": "Expert witnesses testified about engine design",
            },
            {
                "date": "2023-07-15",
                "event": "Court ruling",
                "description": "Court ruled in favor of plaintiff",
            },
            {
                "date": "2023-08-22",
                "event": "Case closed",
                "description": "Settlement finalized and case closed",
            },
        ],
        "offenseArgumentation": "The plaintiff argued that the engine design in the Model X had a fundamental flaw that created a fire risk. They presented evidence of similar incidents and claimed Bayersche was negligent in addressing known issues.",
        "defenseArgumentation": "Our defense argued that the isolated incidents were due to improper maintenance rather than design flaws. We presented extensive testing data showing the engine design met all safety standards.",
        "suggestions": [
            "Consider early settlement in similar cases to avoid negative publicity",
            "Strengthen evidence of customer maintenance records",
            "Develop more comprehensive expert testimony on engine safety features",
        ],
        "outcomePrediction": {
            "cost": "$750,000 - $1,200,000",
            "reputationalLoss": "High",
            "winProbability": "30%",
        },
    },
    "3": {
        "id": "3",
        "title": "Martinez Product Liability Claim",
        "status": "in progress",
        "jurisdiction": "Texas",
        "caseType": "Liability",
        "date": "2024-01-10",
        "relevantLaws": [
            "Texas Transportation Code § 547.004",
            "Texas Deceptive Trade Practices Act",
        ],
        "timeline": [
            {
                "date": "2023-11-15",
                "event": "Initial complaint filed",
                "description": "Plaintiff alleges suspension system failure",
            },
            {
                "date": "2023-12-20",
                "event": "Response filed",
                "description": "Bayersche filed response denying allegations",
            },
            {
                "date": "2024-01-10",
                "event": "Discovery phase initiated",
                "description": "Exchange of documents and evidence begins",
            },
        ],
        "offenseArgumentation": "The plaintiff claims that the suspension system in the Model Y failed during normal driving conditions, causing a rollover accident. They argue that Bayersche was aware of design flaws but failed to address them.",
        "defenseArgumentation": "Our defense is focusing on the vehicle's maintenance history and road conditions at the time of the incident. We are gathering evidence to show the suspension system met all safety standards and was not defective.",
        "suggestions": [
            "Reference the Williams v. AutoTech case where similar claims were successfully defended",
            "Obtain detailed road condition reports from the accident scene",
            "Commission independent testing of the specific suspension components",
        ],
        "outcomePrediction": {
            "cost": "$300,000 - $500,000",
            "reputationalLoss": "Medium",
            "winProbability": "60%",
        },
    },
    "4": {
        "id": "4",
        "title": "Williams Class Action",
        "status": "in progress",
        "jurisdiction": "Florida",
        "caseType": "Liability",
        "date": "2024-02-28",
        "relevantLaws": [
            "Florida Motor Vehicle Safety Act",
            "Florida Deceptive and Unfair Trade Practices Act",
        ],
        "timeline": [
            {
                "date": "2024-01-05",
                "event": "Class action filed",
                "description": "Group of plaintiffs filed class action regarding electrical system",
            },
            {
                "date": "2024-02-10",
                "event": "Motion to dismiss",
                "description": "Bayersche filed motion to dismiss the class action",
            },
            {
                "date": "2024-02-28",
                "event": "Motion denied",
                "description": "Court denied motion to dismiss, case proceeding",
            },
        ],
        "offenseArgumentation": "The class action alleges that the electrical system in multiple Bayersche models has a defect that causes unexpected power loss. Plaintiffs claim this creates a safety hazard and that Bayersche concealed the issue.",
        "defenseArgumentation": "Our defense strategy is to challenge the class certification by demonstrating the diversity of electrical systems across different models and years. We are also gathering data to show the reported incidents are isolated and not indicative of a systemic defect.",
        "suggestions": [
            "Consider partial settlement for older models while contesting newer ones",
            "Develop stronger evidence of system improvements over time",
            "Emphasize the low incident rate compared to total vehicles sold",
        ],
        "outcomePrediction": {
            "cost": "$2,000,000 - $5,000,000",
            "reputationalLoss": "High",
            "winProbability": "45%",
        },
    },
    "5": {
        "id": "5",
        "title": "Garcia v. Bayersche Manufacturing",
        "status": "won",
        "jurisdiction": "Michigan",
        "caseType": "Liability",
        "date": "2023-11-05",
        "relevantLaws": [
            "Michigan Vehicle Code",
            "Michigan Consumer Protection Act",
        ],
        "timeline": [
            {
                "date": "2023-06-12",
                "event": "Initial complaint filed",
                "description": "Plaintiff alleged transmission defect",
            },
            {
                "date": "2023-07-18",
                "event": "Response filed",
                "description": "Bayersche filed response with counterclaims",
            },
            {
                "date": "2023-09-25",
                "event": "Expert testimony",
                "description": "Expert witnesses testified about transmission design",
            },
            {
                "date": "2023-10-30",
                "event": "Court ruling",
                "description": "Court ruled in favor of Bayersche",
            },
            {
                "date": "2023-11-05",
                "event": "Case closed",
                "description": "Case officially closed with favorable outcome",
            },
        ],
        "offenseArgumentation": "The plaintiff claimed that the transmission in their Model Z was defective, causing unexpected shifting and safety hazards. They argued that Bayersche was aware of the issue but failed to address it properly.",
        "defenseArgumentation": "Our defense successfully demonstrated that the transmission functioned as designed and that the plaintiff's issues were due to improper use of the vehicle. We presented extensive testing data and expert testimony to support our position.",
        "suggestions": [
            "Use similar technical evidence approach in future transmission cases",
            "Develop educational materials for customers about proper transmission use",
            "Consider proactive service bulletins for similar customer complaints",
        ],
        "outcomePrediction": {
            "cost": "$200,000 - $300,000",
            "reputationalLoss": "Low",
            "winProbability": "80%",
        },
    }
}

# Initialize database files if they don't exist
def init_db():
    # Always write the sample data to ensure it exists
    with open(CASES_DB_PATH, "w") as f:
        json.dump(SAMPLE_CASE_DATA, f, indent=2)
    print(f"Database initialized with sample data at {CASES_DB_PATH}")

# Database Operations
def get_all_cases() -> List[dict]:
    """Get all cases as a list"""
    try:
        with open(CASES_DB_PATH, "r") as f:
            cases = json.load(f)
        return list(cases.values())
    except (json.JSONDecodeError, FileNotFoundError):
        # If there's a problem with the file, reinitialize it
        init_db()
        with open(CASES_DB_PATH, "r") as f:
            cases = json.load(f)
        return list(cases.values())

def get_case_summaries() -> List[CaseSummary]:
    """Get summaries of all cases for listing"""
    cases = get_all_cases()
    return [
        {
            "id": case["id"], 
            "title": case["title"],
            "status": case["status"],
            "jurisdiction": case["jurisdiction"],
            "caseType": case["caseType"],
            "date": case["date"]
        } for case in cases
    ]

def get_case_by_id(case_id: str) -> Optional[dict]:
    """Get a single case by its ID"""
    with open(CASES_DB_PATH, "r") as f:
        cases = json.load(f)
    return cases.get(case_id)

def get_stats():
    """Get statistics for trends dashboard"""
    cases = get_all_cases()
    
    # Count cases by status
    won_cases = sum(1 for case in cases if case["status"] == "won")
    lost_cases = sum(1 for case in cases if case["status"] == "lost")
    in_progress_cases = sum(1 for case in cases if case["status"] == "in progress")
    total_cases = len(cases)
    
    win_rate = (won_cases / total_cases) * 100 if total_cases > 0 else 0
    loss_rate = (lost_cases / total_cases) * 100 if total_cases > 0 else 0
    
    return {
        "totalCases": total_cases,
        "wonCases": won_cases,
        "lostCases": lost_cases,
        "inProgressCases": in_progress_cases,
        "winRate": round(win_rate, 1),
        "lossRate": round(loss_rate, 1)
    }

def get_car_stats():
    """Get statistics about car models involved in cases"""
    # This is mock data since we don't have actual car models in the case data
    return [
        {"model": "Model S", "count": 35},
        {"model": "Model X", "count": 42},
        {"model": "Model Y", "count": 28},
        {"model": "Model Z", "count": 22}
    ]

def get_part_stats():
    """Get statistics about car parts involved in cases"""
    # This is mock data based on the case descriptions
    return [
        {"part": "Braking System", "count": 32},
        {"part": "Engine", "count": 28},
        {"part": "Suspension", "count": 24},
        {"part": "Electrical System", "count": 26},
        {"part": "Transmission", "count": 17}
    ]

def get_status_stats():
    """Get statistics about case statuses"""
    cases = get_all_cases()
    
    # Count cases by status
    status_counts = {"Won": 0, "Lost": 0, "In Progress": 0}
    
    for case in cases:
        status = case["status"]
        if status == "won":
            status_counts["Won"] += 1
        elif status == "lost":
            status_counts["Lost"] += 1
        elif status == "in progress":
            status_counts["In Progress"] += 1
    
    # Convert to list format for charts
    return [
        {"status": status, "count": count}
        for status, count in status_counts.items()
    ]

# Initialize the database on module import
init_db()