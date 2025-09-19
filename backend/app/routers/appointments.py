from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud, schemas, database

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ CREATE ------------------
@router.post("/", response_model=schemas.Appointment, summary="Create Appointment")
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    # Check if patient & doctor exist
    if not crud.get_patient(db, appointment.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    if not crud.get_doctor(db, appointment.doctor_id):
        raise HTTPException(status_code=404, detail="Doctor not found")
    return crud.create_appointment(db=db, appointment=appointment)

# ------------------ READ ALL ------------------
@router.get("/", response_model=List[schemas.Appointment], summary="Get All Appointments")
def read_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    appointments = crud.get_appointments(db=db, skip=skip, limit=limit)
    if patient_id is not None:
        appointments = [a for a in appointments if a.patient_id == patient_id]
    if doctor_id is not None:
        appointments = [a for a in appointments if a.doctor_id == doctor_id]
    return appointments

# ------------------ READ ONE ------------------
@router.get("/{appointment_id}", response_model=schemas.Appointment, summary="Get Appointment by ID")
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = crud.get_appointment(db=db, appointment_id=appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

# ------------------ UPDATE ------------------
@router.put("/{appointment_id}", response_model=schemas.Appointment, summary="Update Appointment")
def update_appointment(appointment_id: int, appointment: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_appointment(db=db, appointment_id=appointment_id, appointment=appointment)
    if not updated:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated

# ------------------ DELETE ------------------
@router.delete("/{appointment_id}", summary="Delete Appointment")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    success = crud.delete_appointment(db=db, appointment_id=appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"detail": "Appointment deleted successfully"}
