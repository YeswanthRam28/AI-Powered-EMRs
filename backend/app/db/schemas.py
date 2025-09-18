from typing import Optional
from pydantic import BaseModel

# ---------------- Base Schema ----------------
class PatientBase(BaseModel):
    """
    Base schema shared by create and read operations.
    """
    name: str
    age: int
    gender: str
    allergies: Optional[str] = None

# ---------------- Create Schema ----------------
class PatientCreate(PatientBase):
    """
    Schema for creating a new patient.
    Inherits all fields from PatientBase.
    """
    pass

# ---------------- Update Schema ----------------
class PatientUpdate(BaseModel):
    """
    Schema for updating a patient.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    allergies: Optional[str] = None

# ---------------- Read Schema ----------------
class Patient(PatientBase):
    """
    Schema for reading patient data, includes the ID.
    """
    id: int

    class Config:
        orm_mode = True
