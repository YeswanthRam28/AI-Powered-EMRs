from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# ------------------ Load environment ------------------
load_dotenv()  # Loads variables from .env

# ------------------ Import Routers ------------------
from app.routers import patients, doctors, appointments, dashboard, nlp

# =========================================================
# Initialize FastAPI app
# =========================================================
app = FastAPI(
    title="Smart EMR API",
    description="A backend API for managing patients, doctors, appointments, statistics, and AI NLP",
    version="1.0.0"
)

# =========================================================
# Middleware (CORS for frontend integration)
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# Include Routers
# =========================================================
app.include_router(patients.router, tags=["Patients"])
app.include_router(doctors.router, tags=["Doctors"])
app.include_router(appointments.router, tags=["Appointments"])
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(nlp.router, tags=["NLP"])

# =========================================================
# Health check endpoint
# =========================================================
@app.get("/health", summary="Check API Health")
def health():
    """
    Simple endpoint to verify that the API is running.
    """
    return {"status": "ok", "message": "EMR Backend is running!"}
