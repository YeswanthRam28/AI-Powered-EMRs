from fastapi import FastAPI
from app.routers import patients

app = FastAPI(title="Smart EMR API")

# Include patients router
app.include_router(patients.router)

# Optional: health endpoint to check backend separately
@app.get("/api/health")
def health():
    return {"message": "EMR Backend is running!"}
