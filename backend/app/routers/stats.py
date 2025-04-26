from fastapi import APIRouter
from typing import List

from app.db.database import (
    get_stats,
    get_car_stats,
    get_part_stats,
    get_status_stats
)
from app.models.models import TrendStats, CarStats, PartStats, StatusStats

router = APIRouter(
    prefix="/stats",
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=TrendStats)
async def get_trend_stats():
    """
    Get overall case statistics for trends dashboard
    """
    return get_stats()

@router.get("/cars", response_model=List[CarStats])
async def get_car_statistics():
    """
    Get statistics about affected car models
    """
    return get_car_stats()

@router.get("/parts", response_model=List[PartStats])
async def get_part_statistics():
    """
    Get statistics about affected car parts
    """
    return get_part_stats()

@router.get("/status", response_model=List[StatusStats])
async def get_status_statistics():
    """
    Get statistics about case statuses
    """
    return get_status_stats()