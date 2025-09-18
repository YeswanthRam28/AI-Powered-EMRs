from fastapi import FastAPI
from app.routers import patients

app = FastAPI(title="Smart EMR API")

@app.get("/")  # 👈 root endpoint
def root():
    return {"message": "Hello, EMR Backend is running!"}

# include patients router
app.include_router(patients.router)
