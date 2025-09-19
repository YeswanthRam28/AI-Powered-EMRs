from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

# ------------------ Load environment variables ------------------
load_dotenv()

# ------------------ Import API Routers ------------------
from app.routers import patients, doctors, appointments, dashboard, nlp

# =========================================================
# Initialize FastAPI App
# =========================================================
app = FastAPI(
    title="Smart EMR API",
    description="Backend API for managing patients, doctors, appointments, dashboard stats, and AI NLP tasks",
    version="1.0.0"
)

# =========================================================
# Middleware: CORS for frontend integration
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =========================================================
# Include API Routers
# =========================================================
app.include_router(patients.router, tags=["Patients"])
app.include_router(doctors.router, tags=["Doctors"])
app.include_router(appointments.router, tags=["Appointments"])
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(nlp.router, tags=["NLP"])

# =========================================================
# Frontend Integration
# =========================================================
# Absolute path to the frontend folder (outside backend)
frontend_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "frontend"
)

# Mount static files for frontend
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Serve the main dashboard page
@app.get("/", summary="Frontend Dashboard", include_in_schema=False)
def serve_dashboard():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Frontend index.html not found"}

# =========================================================
# Health Check Endpoint
# =========================================================
@app.get("/health", summary="Check API Health")
def health():
    """
    Endpoint to verify that the API is running.
    """
    return {"status": "ok", "message": "EMR Backend is running!"}
