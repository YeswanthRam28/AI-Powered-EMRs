from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Dict
from app.db import models, database

# =========================================================
# Router configuration
# =========================================================
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# ---------------- Database Dependency ----------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Dashboard Endpoint ----------------
@router.get("/", summary="Get EMR Dashboard statistics")
def get_dashboard_stats(db: Session = Depends(get_db)) -> Dict:
    """
    Returns overall statistics for the EMR system:
    - Total patients
    - Total doctors
    - Total appointments
    - Appointments per doctor
    - Patients per doctor
    - Monthly appointments count
    """
    # ---------------- Total Counts ----------------
    total_patients = db.query(func.count(models.Patient.id)).scalar()
    total_doctors = db.query(func.count(models.Doctor.id)).scalar()
    total_appointments = db.query(func.count(models.Appointment.id)).scalar()

    # ---------------- Appointments per Doctor ----------------
    appointments_per_doctor = (
        db.query(models.Doctor.name, func.count(models.Appointment.id))
        .join(models.Appointment, models.Doctor.id == models.Appointment.doctor_id, isouter=True)
        .group_by(models.Doctor.id)
        .all()
    )
    appointments_per_doctor_dict = {name: count for name, count in appointments_per_doctor}

    # ---------------- Patients per Doctor ----------------
    patients_per_doctor = (
        db.query(models.Doctor.name, func.count(func.distinct(models.Appointment.patient_id)))
        .join(models.Appointment, models.Doctor.id == models.Appointment.doctor_id, isouter=True)
        .group_by(models.Doctor.id)
        .all()
    )
    patients_per_doctor_dict = {name: count for name, count in patients_per_doctor}

    # ---------------- Monthly Appointments ----------------
    monthly_appointments = (
        db.query(
            extract("year", models.Appointment.date).label("year"),
            extract("month", models.Appointment.date).label("month"),
            func.count(models.Appointment.id)
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )
    monthly_appointments_dict = {
        f"{int(year)}-{int(month):02d}": count for year, month, count in monthly_appointments
    }

    # ---------------- Return Dashboard Data ----------------
    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "appointments_per_doctor": appointments_per_doctor_dict,
        "patients_per_doctor": patients_per_doctor_dict,
        "monthly_appointments": monthly_appointments_dict
    }
