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

    # Normalize status for win/loss/in progress/settled
    won_cases = sum(
        1
        for case in cases
        if str(case.get("status", "")).strip().lower() == "in favour of defendant"
    )
    lost_cases = sum(
        1
        for case in cases
        if str(case.get("status", "")).strip().lower() == "in favour of plaintiff"
    )
    settled_cases = sum(
        1 for case in cases if str(case.get("status", "")).strip().lower() == "settled"
    )
    in_progress_cases = sum(
        1 for case in cases if "progress" in str(case.get("status", "")).strip().lower()
    )
    total_cases = len(cases)

    win_rate = (won_cases / total_cases) * 100 if total_cases > 0 else 0
    loss_rate = (lost_cases / total_cases) * 100 if total_cases > 0 else 0

    return {
        "totalCases": total_cases,
        "wonCases": won_cases,
        "lostCases": lost_cases,
        "settledCases": settled_cases,
        "inProgressCases": in_progress_cases,
        "winRate": round(win_rate, 1),
        "lossRate": round(loss_rate, 1),
    }


def get_car_stats():
    """Get statistics about car models involved in cases"""
    cases = get_all_cases()
    car_counts = {}
    for case in cases:
        car = case.get("affectedCar", None)
        if car and car != "Not specified":
            car_counts[car] = car_counts.get(car, 0) + 1
    return [{"model": model, "count": count} for model, count in car_counts.items()]


def get_part_stats():
    """Get statistics about car parts involved in cases"""
    cases = get_all_cases()
    part_counts = {}
    for case in cases:
        part = case.get("affectedPart", None)
        if part and part != "Not specified":
            part_counts[part] = part_counts.get(part, 0) + 1
    return [{"part": part, "count": count} for part, count in part_counts.items()]


def get_status_stats():
    cases = get_all_cases()
    status_counts = {
        "In favour of defendant": 0,
        "In favour of plaintiff": 0,
        "In Progress": 0,
        "Settled": 0,
    }

    for case in cases:
        status = str(case.get("status", "")).strip().lower()
        if status == "in favour of defendant":
            status_counts["In favour of defendant"] += 1
        elif status == "in favour of plaintiff":
            status_counts["In favour of plaintiff"] += 1
        elif status == "settled":
            status_counts["Settled"] += 1
        elif "progress" in status:
            status_counts["In Progress"] += 1

    return [
        {"status": status, "count": count}
        for status, count in status_counts.items()
        if count > 0
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
