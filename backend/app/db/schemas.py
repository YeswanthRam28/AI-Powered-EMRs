from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    allergies: str | None = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True
