import datetime
from sqlalchemy.orm import Session
from . import models

def seed_database(db: Session):
    if db.query(models.Candidate).count() > 0:
        return

    candidates_data = [
        {"name": "Marlon Reynolds", "stage": "Applying Period", "application_date": datetime.date(2023, 10, 29), "overall_score": 3.5, "referred": True, "assessment_status": "Completed"},
        {"name": "Regina Hane", "stage": "Applying Period", "application_date": datetime.date(2023, 10, 29), "overall_score": 2.0, "referred": False, "assessment_status": "Completed"},
        {"name": "Curtis Baumbach", "stage": "Applying Period", "application_date": datetime.date(2023, 10, 29), "overall_score": 3.0, "referred": True, "assessment_status": "Completed"},
        {"name": "Jaime Anderson", "stage": "Applying Period", "application_date": datetime.date(2023, 10, 29), "overall_score": None, "referred": False, "assessment_status": "Not Started"},

        {"name": "Kristi Sipes", "stage": "Screening", "application_date": datetime.date(2023, 10, 20), "overall_score": 3.5, "referred": False, "assessment_status": "Completed"},
        {"name": "Randy Dibbert", "stage": "Screening", "application_date": datetime.date(2023, 10, 18), "overall_score": 3.5, "referred": False, "assessment_status": "Completed"},
        {"name": "Jane Anderson", "stage": "Screening", "application_date": datetime.date(2023, 10, 18), "overall_score": None, "referred": False, "assessment_status": "Not Started"},
        {"name": "Shelia Doyle", "stage": "Screening", "application_date": datetime.date(2023, 10, 13), "overall_score": 4.5, "referred": True, "assessment_status": "Completed"},
        {"name": "Cassandra Hartmann", "stage": "Screening", "application_date": datetime.date(2023, 10, 10), "overall_score": None, "referred": False, "assessment_status": "Not Started"},

        {"name": "Cameron Dickens", "stage": "Interview", "application_date": datetime.date(2023, 9, 3), "overall_score": 4.0, "referred": False, "assessment_status": "Completed"},
        {"name": "Merle Vandervort", "stage": "Interview", "application_date": datetime.date(2023, 9, 9), "overall_score": 4.0, "referred": False, "assessment_status": "Completed"},
        {"name": "Jasmine Wiza", "stage": "Interview", "application_date": datetime.date(2023, 9, 10), "overall_score": None, "referred": False, "assessment_status": "Not Started"},

        {"name": "Lola Kirlin", "stage": "Test", "application_date": datetime.date(2023, 9, 3), "overall_score": 4.5, "referred": True, "assessment_status": "Completed"},
        {"name": "Virgil Larkin", "stage": "Test", "application_date": datetime.date(2023, 9, 3), "overall_score": None, "referred": False, "assessment_status": "Not Started"}
    ]

    for data in candidates_data:
        candidate = models.Candidate(**data)
        db.add(candidate)
    
    db.commit()
