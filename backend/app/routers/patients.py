from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud, database, models, schemas

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create patient
@router.post("/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

# List patients
@router.get("/", response_model=list[schemas.Patient])
def list_patients(db: Session = Depends(get_db)):
    return crud.get_patients(db)

# Get single patient
@router.get("/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Update patient
@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(patient_id: int, updated_data: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient = crud.update_patient(db, patient_id, updated_data)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Delete patient
@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_patient(db, patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}
