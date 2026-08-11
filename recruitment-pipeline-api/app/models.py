from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from .database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    stage = Column(String, nullable=False)
    application_date = Column(Date, nullable=False)
    overall_score = Column(Float, nullable=True)
    referred = Column(Boolean, default=False)
    assessment_status = Column(String, default="Not Started")
