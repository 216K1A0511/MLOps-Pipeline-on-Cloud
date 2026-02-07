from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from typing import Dict, List
import os
from dotenv import load_dotenv
import uvicorn

# Load env variables
load_dotenv()

app = FastAPI(title="Gemini MLOps API")

# Initialize Gemini Client
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)
model_name = 'gemini-2.0-flash'

class PredictionRequest(BaseModel):
    features: Dict[str, float]
    task: str = "classification"

class TrainingRequest(BaseModel):
    examples: List[Dict]
    task_type: str

@app.get("/")
def read_root():
    return {"message": "Gemini MLOps API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "gemini-pro-latest"}

@app.post("/predict")
def predict(request: PredictionRequest):
    """Make prediction using Gemini"""
    if not api_key:
         raise HTTPException(status_code=500, detail="Server misconfigured: Missing API Key")
    try:
        prompt = f"""
    Classify based on features: {request.features}
    Return ONLY 'Positive' or 'Negative'
    """
        
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return {"prediction": response.text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
def train_model(request: TrainingRequest):
    """Start training pipeline"""
    # In production, this would trigger async training
    return {
        "message": "Training pipeline triggered",
        "examples": len(request.examples),
        "task": request.task_type,
        "status": "queued"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
