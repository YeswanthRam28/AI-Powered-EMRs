from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import models, schemas

# ---------------- Create ----------------
def create_patient(db: Session, patient: schemas.PatientCreate) -> models.Patient:
    """
    Create a new patient record in the database.
    """
    db_patient = models.Patient(
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        allergies=patient.allergies
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# ---------------- Read ----------------
def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[models.Patient]:
    """
    Retrieve a list of patients with optional pagination.
    """
    return db.query(models.Patient).offset(skip).limit(limit).all()

def get_patient(db: Session, patient_id: int) -> Optional[models.Patient]:
    """
    Retrieve a single patient by their ID.
    """
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

# ---------------- Update ----------------
def update_patient(db: Session, patient_id: int, patient: schemas.PatientUpdate) -> Optional[models.Patient]:
    """
    Update patient details. Only fields provided in `patient` will be updated.
    """
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return None

    # Update only the fields provided (exclude unset fields)
    for field, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, field, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient

# ---------------- Delete ----------------
def delete_patient(db: Session, patient_id: int) -> bool:
    """
    Delete a patient by ID.
    Returns True if deleted, None if the patient was not found.
    """
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return None

    db.delete(db_patient)
    db.commit()
    return True
