from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import patients, doctors, appointments, dashboard  # Added dashboard

# =========================================================
# Initialize FastAPI app
# =========================================================
app = FastAPI(
    title="Smart EMR API",
    description="A backend API for managing patients, doctors, appointments, and statistics",
    version="1.0.0"
)

# =========================================================
# Middleware (CORS for frontend integration)
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# Include routers
# =========================================================
app.include_router(patients.router, tags=["Patients"])
app.include_router(doctors.router, tags=["Doctors"])
app.include_router(appointments.router, tags=["Appointments"])
app.include_router(dashboard.router, tags=["Dashboard"])  # Added dashboard

# =========================================================
# Health check endpoint
# =========================================================
@app.get("/health", summary="Check API Health")
def health():
    """
    Simple endpoint to verify that the API is running.
    Returns a success message.
    """
    return {"status": "ok", "message": "EMR Backend is running!"}
