from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
import os
import requests
import json
from dotenv import load_dotenv

# ------------------- Load environment -------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in environment variables.")

# ------------------- FastAPI Router -------------------
router = APIRouter(
    prefix="/nlp",
    tags=["NLP"]
)

# ------------------- Request Model -------------------
class NLPRequest(BaseModel):
    text: str
    task: Literal[
        "summarize", 
        "keywords", 
        "insights", 
        "diagnosis", 
        "treatment_plan", 
        "risk_factors", 
        "red_flags", 
        "translate", 
        "sentiment", 
        "ner"
    ]

# ------------------- Response Model -------------------
class NLPResponse(BaseModel):
    task: str
    input_text: str
    result: str

# ------------------- Storage -------------------
RESULTS_FILE = "nlp_results.json"

def save_result(result: dict):
    """Append result to JSON file."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(result)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_results():
    """Load saved results."""
    if not os.path.exists(RESULTS_FILE):
        return []
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ------------------- Helper Function -------------------
def call_gemini(prompt: str, model: str = "gemini-1.5-flash") -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    params = {"key": GOOGLE_API_KEY}

    response = requests.post(url, headers=headers, json=payload, params=params)

    if response.status_code != 200:
        raise RuntimeError(f"Gemini API error: {response.text}")

    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected Gemini response: {data}")

# ------------------- NLP POST Endpoint -------------------
@router.post("/", response_model=NLPResponse, summary="Process medical text using Gemini AI")
def process_text(request: NLPRequest):
    task_prompts = {
        "summarize": f"Summarize the following medical note concisely:\n{request.text}",
        "keywords": f"Extract all important medical keywords from this medical note:\n{request.text}",
        "insights": f"Analyze the following medical note and provide actionable insights or recommendations:\n{request.text}",
        "diagnosis": f"Based on the following medical note, predict possible diagnoses:\n{request.text}",
        "treatment_plan": f"Provide a possible treatment plan for the following note:\n{request.text}",
        "risk_factors": f"Identify all risk factors from this patient's medical note:\n{request.text}",
        "red_flags": f"Identify any urgent red flags in this note:\n{request.text}",
        "translate": f"Translate the following medical note into Tamil:\n{request.text}",
        "sentiment": f"Analyze the sentiment (positive, negative, urgent, neutral) of this note:\n{request.text}",
        "ner": f"Extract structured medical entities (diseases, symptoms, drugs, measurements) from this note:\n{request.text}"
    }

    prompt = task_prompts.get(request.task)
    if not prompt:
        raise HTTPException(status_code=400, detail="Invalid task type.")

    try:
        result_text = call_gemini(prompt)
        result = NLPResponse(task=request.task, input_text=request.text, result=result_text)
        save_result(result.dict())  # Save executed result
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# ------------------- NLP GET Endpoint -------------------
@router.get("/", summary="Fetch all saved NLP results")
def get_all_results():
    results = load_results()
    return {"count": len(results), "results": results}
