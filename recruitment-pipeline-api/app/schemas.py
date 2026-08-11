from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class CandidateBase(BaseModel):
    name: str
    stage: str
    application_date: date
    overall_score: Optional[float] = None
    referred: bool = False
    assessment_status: str = "Not Started"

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    stage: Optional[str] = None
    application_date: Optional[date] = None
    overall_score: Optional[float] = None
    referred: Optional[bool] = None
    assessment_status: Optional[str] = None

class CandidateResponse(CandidateBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
