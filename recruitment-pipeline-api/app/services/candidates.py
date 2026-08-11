from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas

def get_candidates(
    db: Session,
    stage: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    sort_by: Optional[str] = None,
    order: str = "asc"
) -> List[models.Candidate]:
    query = db.query(models.Candidate)
    
    if stage:
        query = query.filter(models.Candidate.stage == stage)
        
    if sort_by:
        if sort_by == "application_date":
            sort_column = models.Candidate.application_date
        elif sort_by == "overall_score":
            sort_column = models.Candidate.overall_score
        else:
            sort_column = None
            
        if sort_column is not None:
            if order.lower() == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

    return query.offset(skip).limit(limit).all()

def get_candidate(db: Session, candidate_id: int) -> Optional[models.Candidate]:
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

def create_candidate(db: Session, candidate: schemas.CandidateCreate) -> models.Candidate:
    db_candidate = models.Candidate(**candidate.model_dump())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def update_candidate(
    db: Session, db_candidate: models.Candidate, candidate_update: schemas.CandidateUpdate
) -> models.Candidate:
    update_data = candidate_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_candidate, key, value)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def update_candidate_stage(db: Session, db_candidate: models.Candidate, stage: str) -> models.Candidate:
    db_candidate.stage = stage
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def delete_candidate(db: Session, db_candidate: models.Candidate) -> None:
    db.delete(db_candidate)
    db.commit()
