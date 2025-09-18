from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel

# =========================================================
# Patient Schemas
# =========================================================
class PatientBase(BaseModel):
    """Base schema shared by create and read operations."""
    name: str
    age: int
    gender: str
    allergies: Optional[str] = None

class PatientCreate(PatientBase):
    """Schema for creating a new patient."""
    pass

class PatientUpdate(BaseModel):
    """Schema for updating a patient (all fields optional)."""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    allergies: Optional[str] = None

class Patient(PatientBase):
    """Schema for reading patient data (includes ID)."""
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode

# =========================================================
# Doctor Schemas
# =========================================================
class DoctorBase(BaseModel):
    """Base schema for doctors."""
    name: str
    specialty: str
    contact: str

class DoctorCreate(DoctorBase):
    """Schema for creating a doctor."""
    pass

class DoctorUpdate(BaseModel):
    """Schema for updating a doctor (all fields optional)."""
    name: Optional[str] = None
    specialty: Optional[str] = None
    contact: Optional[str] = None

class Doctor(DoctorBase):
    """Schema for reading doctor data (includes ID)."""
    id: int

    class Config:
        from_attributes = True

# =========================================================
# Appointment Schemas
# =========================================================
class AppointmentBase(BaseModel):
    """Base schema for appointments."""
    patient_id: int
    doctor_id: int
    date: datetime
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    """Schema for creating an appointment."""
    pass

class AppointmentUpdate(BaseModel):
    """Schema for updating an appointment (all fields optional)."""
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

class Appointment(AppointmentBase):
    """Schema for reading appointment data (includes ID)."""
    id: int

    class Config:
        from_attributes = True

# =========================================================
# Dashboard / Statistics Schema
# =========================================================
class DashboardStats(BaseModel):
    """Schema representing aggregated statistics for the dashboard."""
    total_patients: int
    patients_by_gender: Dict[str, int]
    total_doctors: int
    doctors_by_specialty: Dict[str, int]
    total_appointments: int
    appointments_by_doctor: Dict[int, int]
    appointments_by_patient: Dict[int, int]
    upcoming_appointments: int
    past_appointments: int
