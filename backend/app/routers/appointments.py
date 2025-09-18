from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud, schemas, database

# =========================================================
# Router configuration
# =========================================================
router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================================================
# CREATE
# =========================================================
@router.post("/", response_model=schemas.Appointment, summary="Create Appointment")
def create_appointment(
    appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)
):
    """
    Create a new appointment.
    Raises 404 if the patient or doctor does not exist.
    """
    return crud.create_appointment(db=db, appointment=appointment)

# =========================================================
# READ ALL
# =========================================================
@router.get("/", response_model=List[schemas.Appointment], summary="Get All Appointments")
def read_appointments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=500, description="Maximum number of records to return"),
    patient_id: Optional[int] = Query(None, description="Filter by patient ID"),
    doctor_id: Optional[int] = Query(None, description="Filter by doctor ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all appointments with optional pagination and filtering by patient or doctor.
    """
    appointments = crud.get_appointments(db=db, skip=skip, limit=limit)

    if patient_id is not None:
        appointments = [a for a in appointments if a.patient_id == patient_id]
    if doctor_id is not None:
        appointments = [a for a in appointments if a.doctor_id == doctor_id]

    return appointments

# =========================================================
# READ ONE
# =========================================================
@router.get("/{appointment_id}", response_model=schemas.Appointment, summary="Get Appointment by ID")
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single appointment by its ID.
    Raises 404 if not found.
    """
    db_appointment = crud.get_appointment(db=db, appointment_id=appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

# =========================================================
# UPDATE
# =========================================================
@router.put("/{appointment_id}", response_model=schemas.Appointment, summary="Update Appointment")
def update_appointment(
    appointment_id: int, appointment: schemas.AppointmentUpdate, db: Session = Depends(get_db)
):
    """
    Update an appointment by ID.
    Only the provided fields in the request body will be updated.
    Raises 404 if the appointment does not exist.
    """
    db_appointment = crud.update_appointment(db=db, appointment_id=appointment_id, appointment=appointment)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

# =========================================================
# DELETE
# =========================================================
@router.delete("/{appointment_id}", summary="Delete Appointment")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Delete an appointment by its ID.
    Raises 404 if the appointment does not exist.
    """
    success = crud.delete_appointment(db=db, appointment_id=appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"detail": "Appointment deleted successfully"}
