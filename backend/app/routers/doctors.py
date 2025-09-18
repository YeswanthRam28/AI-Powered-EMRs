from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud, schemas, database

# =========================================================
# Router configuration
# =========================================================
router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
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
@router.post("/", response_model=schemas.Doctor, summary="Create a new doctor")
def create_doctor(
    doctor: schemas.DoctorCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new doctor record.
    """
    return crud.create_doctor(db=db, doctor=doctor)

# =========================================================
# READ ALL
# =========================================================
@router.get("/", response_model=List[schemas.Doctor], summary="List all doctors")
def read_doctors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=500, description="Maximum number of records to return"),
    name: Optional[str] = Query(None, description="Filter doctors by name"),
    specialty: Optional[str] = Query(None, description="Filter doctors by specialty"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all doctors with optional pagination and filtering by name or specialty.
    """
    doctors = crud.get_doctors(db=db, skip=skip, limit=limit)
    
    # Filter in memory for optional search
    if name:
        doctors = [doc for doc in doctors if name.lower() in doc.name.lower()]
    if specialty:
        doctors = [doc for doc in doctors if specialty.lower() in doc.specialty.lower()]
    
    return doctors

# =========================================================
# READ ONE
# =========================================================
@router.get("/{doctor_id}", response_model=schemas.Doctor, summary="Get doctor by ID")
def read_doctor(
    doctor_id: int, 
    db: Session = Depends(get_db)
):
    """
    Retrieve a single doctor by ID.
    """
    db_doctor = crud.get_doctor(db=db, doctor_id=doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

# =========================================================
# UPDATE
# =========================================================
@router.put("/{doctor_id}", response_model=schemas.Doctor, summary="Update doctor")
def update_doctor(
    doctor_id: int, 
    updated_data: schemas.DoctorUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update a doctor's information. Only provided fields will be updated.
    """
    db_doctor = crud.update_doctor(db=db, doctor_id=doctor_id, doctor=updated_data)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

# =========================================================
# DELETE
# =========================================================
@router.delete("/{doctor_id}", summary="Delete doctor")
def delete_doctor(
    doctor_id: int, 
    db: Session = Depends(get_db)
):
    """
    Delete a doctor by ID.
    """
    success = crud.delete_doctor(db=db, doctor_id=doctor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deleted successfully"}
