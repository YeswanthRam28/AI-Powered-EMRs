from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud, schemas, database

# =========================================================
# Router configuration
# =========================================================
router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)

# =========================================================
# Dependency to get DB session
# =========================================================
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================================================
# CREATE
# =========================================================
@router.post("/", response_model=schemas.Patient, summary="Create a new patient")
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """
    Create a new patient record.
    """
    return crud.create_patient(db=db, patient=patient)

# =========================================================
# READ ALL (with optional filters)
# =========================================================
@router.get("/", response_model=List[schemas.Patient], summary="List patients")
def list_patients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=500, description="Maximum number of records to return"),
    name: Optional[str] = Query(None, description="Filter patients by name"),
    age: Optional[int] = Query(None, description="Filter patients by age"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of patients with optional pagination and filtering by name or age.
    """
    patients = crud.get_patients(db=db, skip=skip, limit=limit)

    if name:
        patients = [p for p in patients if name.lower() in p.name.lower()]
    if age is not None:
        patients = [p for p in patients if p.age == age]

    return patients

# =========================================================
# READ ONE
# =========================================================
@router.get("/{patient_id}", response_model=schemas.Patient, summary="Get patient by ID")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single patient by their ID.
    """
    patient = crud.get_patient(db=db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# =========================================================
# UPDATE
# =========================================================
@router.put("/{patient_id}", response_model=schemas.Patient, summary="Update patient")
def update_patient(patient_id: int, updated_data: schemas.PatientUpdate, db: Session = Depends(get_db)):
    """
    Update a patient's information. Only the fields provided will be updated.
    """
    patient = crud.update_patient(db=db, patient_id=patient_id, patient=updated_data)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# =========================================================
# DELETE
# =========================================================
@router.delete("/{patient_id}", summary="Delete patient")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Delete a patient record by ID.
    """
    deleted = crud.delete_patient(db=db, patient_id=patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}
