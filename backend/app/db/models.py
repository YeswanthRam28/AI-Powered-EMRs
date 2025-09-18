from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

# ============================================================
# Patient Model
# ============================================================
class Patient(Base):
    """
    Database model for storing patient records.
    """
    __tablename__ = "patients"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    age: int = Column(Integer, nullable=False)
    gender: str = Column(String, nullable=False)
    allergies: str = Column(String, nullable=True)

    # Relationship to appointments (cascade deletes appointments if patient is deleted)
    appointments = relationship(
        "Appointment", 
        back_populates="patient", 
        cascade="all, delete-orphan"
    )


# ============================================================
# Doctor Model
# ============================================================
class Doctor(Base):
    """
    Database model for storing doctor records.
    """
    __tablename__ = "doctors"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    specialty: str = Column(String, nullable=False)
    contact: str = Column(String, nullable=False)

    # Relationship to appointments (cascade deletes appointments if doctor is deleted)
    appointments = relationship(
        "Appointment", 
        back_populates="doctor", 
        cascade="all, delete-orphan"
    )


# ============================================================
# Appointment Model
# ============================================================
class Appointment(Base):
    """
    Database model for storing appointment records.
    """
    __tablename__ = "appointments"

    id: int = Column(Integer, primary_key=True, index=True)
    patient_id: int = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id: int = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    date: DateTime = Column(DateTime, nullable=False)
    notes: str = Column(String, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
