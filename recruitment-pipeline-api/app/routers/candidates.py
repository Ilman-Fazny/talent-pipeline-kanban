from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas
from ..database import get_db
from ..services import candidates as candidate_service

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
)

@router.post("", response_model=schemas.CandidateResponse)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    return candidate_service.create_candidate(db, candidate)

@router.get("", response_model=List[schemas.CandidateResponse])
def list_candidates(
    stage: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    sort_by: Optional[str] = None,
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return candidate_service.get_candidates(
        db, stage=stage, skip=skip, limit=limit, sort_by=sort_by, order=order
    )

@router.get("/{id}", response_model=schemas.CandidateResponse)
def get_candidate(id: int, db: Session = Depends(get_db)):
    db_candidate = candidate_service.get_candidate(db, id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.put("/{id}", response_model=schemas.CandidateResponse)
def update_candidate(id: int, candidate: schemas.CandidateUpdate, db: Session = Depends(get_db)):
    db_candidate = candidate_service.get_candidate(db, id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate_service.update_candidate(db, db_candidate, candidate)

@router.delete("/{id}")
def delete_candidate(id: int, db: Session = Depends(get_db)):
    db_candidate = candidate_service.get_candidate(db, id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    candidate_service.delete_candidate(db, db_candidate)
    return {"message": "Candidate deleted successfully"}

@router.patch("/{id}/stage", response_model=schemas.CandidateResponse)
def update_candidate_stage(id: int, stage: str = Body(..., embed=True), db: Session = Depends(get_db)):
    db_candidate = candidate_service.get_candidate(db, id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate_service.update_candidate_stage(db, db_candidate, stage)
