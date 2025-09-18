from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from fastapi import HTTPException
from datetime import datetime
from app.db import models, schemas

# =========================================================
# CRUD operations for Patients
# =========================================================

def create_patient(db: Session, patient: schemas.PatientCreate) -> models.Patient:
    db_patient = models.Patient(
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        allergies=patient.allergies,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[models.Patient]:
    return db.query(models.Patient).offset(skip).limit(limit).all()

def get_patient(db: Session, patient_id: int) -> Optional[models.Patient]:
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def update_patient(db: Session, patient_id: int, patient: schemas.PatientUpdate) -> Optional[models.Patient]:
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return None
    for field, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, field, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int) -> bool:
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return False
    db.delete(db_patient)
    db.commit()
    return True

# =========================================================
# CRUD operations for Doctors
# =========================================================

def create_doctor(db: Session, doctor: schemas.DoctorCreate) -> models.Doctor:
    db_doctor = models.Doctor(
        name=doctor.name,
        specialty=doctor.specialty,
        contact=doctor.contact,
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_doctors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Doctor]:
    return db.query(models.Doctor).offset(skip).limit(limit).all()

def get_doctor(db: Session, doctor_id: int) -> Optional[models.Doctor]:
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

def update_doctor(db: Session, doctor_id: int, doctor: schemas.DoctorUpdate) -> Optional[models.Doctor]:
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        return None
    for field, value in doctor.dict(exclude_unset=True).items():
        setattr(db_doctor, field, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: int) -> bool:
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        return False
    db.delete(db_doctor)
    db.commit()
    return True

# =========================================================
# CRUD operations for Appointments
# =========================================================

def create_appointment(db: Session, appointment: schemas.AppointmentCreate) -> models.Appointment:
    if not db.query(models.Patient).filter(models.Patient.id == appointment.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")
    if not db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first():
        raise HTTPException(status_code=404, detail="Doctor not found")

    db_appointment = models.Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        date=appointment.date,
        notes=appointment.notes,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments(db: Session, skip: int = 0, limit: int = 100) -> List[models.Appointment]:
    return db.query(models.Appointment).offset(skip).limit(limit).all()

def get_appointment(db: Session, appointment_id: int) -> Optional[models.Appointment]:
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()

def update_appointment(db: Session, appointment_id: int, appointment: schemas.AppointmentUpdate) -> Optional[models.Appointment]:
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        return None

    if appointment.patient_id and not db.query(models.Patient).filter(models.Patient.id == appointment.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")
    if appointment.doctor_id and not db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first():
        raise HTTPException(status_code=404, detail="Doctor not found")

    for field, value in appointment.dict(exclude_unset=True).items():
        setattr(db_appointment, field, value)

    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int) -> bool:
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        return False
    db.delete(db_appointment)
    db.commit()
    return True

# =========================================================
# Dashboard / Statistics Feature
# =========================================================

def get_dashboard_stats(db: Session) -> schemas.DashboardStats:
    patients = db.query(models.Patient).all()
    doctors = db.query(models.Doctor).all()
    appointments = db.query(models.Appointment).all()

    # Patients by gender
    patients_by_gender: Dict[str, int] = {}
    for p in patients:
        patients_by_gender[p.gender] = patients_by_gender.get(p.gender, 0) + 1

    # Doctors by specialty
    doctors_by_specialty: Dict[str, int] = {}
    for d in doctors:
        doctors_by_specialty[d.specialty] = doctors_by_specialty.get(d.specialty, 0) + 1

    # Appointments by doctor and patient
    appointments_by_doctor: Dict[int, int] = {}
    appointments_by_patient: Dict[int, int] = {}

    now = datetime.now()
    upcoming_appointments = 0
    past_appointments = 0

    for a in appointments:
        appointments_by_doctor[a.doctor_id] = appointments_by_doctor.get(a.doctor_id, 0) + 1
        appointments_by_patient[a.patient_id] = appointments_by_patient.get(a.patient_id, 0) + 1
        if a.date > now:
            upcoming_appointments += 1
        else:
            past_appointments += 1

    return schemas.DashboardStats(
        total_patients=len(patients),
        patients_by_gender=patients_by_gender,
        total_doctors=len(doctors),
        doctors_by_specialty=doctors_by_specialty,
        total_appointments=len(appointments),
        appointments_by_doctor=appointments_by_doctor,
        appointments_by_patient=appointments_by_patient,
        upcoming_appointments=upcoming_appointments,
        past_appointments=past_appointments
    )
