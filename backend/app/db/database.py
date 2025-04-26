import json
import os
from typing import Dict, List, Optional
from app.models.models import Case, CaseSummary

# Paths
DB_DIR = os.path.dirname(os.path.abspath(__file__))
CASES_DB_PATH = os.path.join(DB_DIR, "cases.json")


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
    return cases


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
        "lossRate": round(loss_rate, 1),
    }


def get_car_stats():
    """Get statistics about car models involved in cases"""
    # This is mock data since we don't have actual car models in the case data
    return [
        {"model": "Model S", "count": 35},
        {"model": "Model X", "count": 42},
        {"model": "Model Y", "count": 28},
        {"model": "Model Z", "count": 22},
    ]


def get_part_stats():
    """Get statistics about car parts involved in cases"""
    # This is mock data based on the case descriptions
    return [
        {"part": "Braking System", "count": 32},
        {"part": "Engine", "count": 28},
        {"part": "Suspension", "count": 24},
        {"part": "Electrical System", "count": 26},
        {"part": "Transmission", "count": 17},
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
        {"status": status, "count": count} for status, count in status_counts.items()
    ]


def add_new_case(case_id: str, case_data: Dict) -> bool:
    """Add a new case to the database

    Args:
        case_id: The ID of the new case
        case_data: The case data to add

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load the current cases
        with open(CASES_DB_PATH, "r") as f:
            cases = json.load(f)

        # Add the new case
        cases[case_id] = case_data

        # Save the updated cases
        with open(CASES_DB_PATH, "w") as f:
            json.dump(cases, f, indent=2)

        return True
    except Exception as e:
        print(f"Error adding new case: {e}")
        return False
