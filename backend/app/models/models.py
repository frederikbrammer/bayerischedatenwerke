from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from datetime import date

class TimelineEvent(BaseModel):
    date: str
    event: str
    description: str

class OutcomePrediction(BaseModel):
    cost: str
    reputationalLoss: str
    winProbability: str

class Case(BaseModel):
    id: str
    title: str
    status: Literal["won", "lost", "in progress"]
    jurisdiction: str
    caseType: str
    date: str
    relevantLaws: Optional[List[str]] = []
    timeline: Optional[List[TimelineEvent]] = []
    offenseArgumentation: Optional[str] = None
    defenseArgumentation: Optional[str] = None
    suggestions: Optional[List[str]] = []
    outcomePrediction: Optional[OutcomePrediction] = None

class CaseSummary(BaseModel):
    id: str
    title: str
    status: Literal["won", "lost", "in progress"]
    jurisdiction: str
    caseType: str
    date: str

class TrendStats(BaseModel):
    totalCases: int
    wonCases: int
    lostCases: int
    inProgressCases: int
    winRate: float
    lossRate: float

class CarStats(BaseModel):
    model: str
    count: int

class PartStats(BaseModel):
    part: str
    count: int

class StatusStats(BaseModel):
    status: str
    count: int
    
class CreateCaseRequest(BaseModel):
    title: str
    status: Literal["won", "lost", "in progress"]
    jurisdiction: str
    caseType: str
    date: str
    relevantLaws: Optional[List[str]] = []
    timeline: Optional[List[TimelineEvent]] = []
    suggestions: Optional[List[str]] = []
    documentContent: Optional[str] = None
    
class CaseResponse(BaseModel):
    id: str