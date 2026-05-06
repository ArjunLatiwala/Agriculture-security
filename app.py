from fastapi import FastAPI
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Crop Yield API")

class PredictionRequest(BaseModel):
    nitrogen: int = Field(..., ge=0, le=500, description="Nitrogen PPM")
    phosphorus: int = Field(..., ge=0, le=200, description="Phosphorus PPM")

class PredictionResponse(BaseModel):
    yield_prediction: float
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    result = (request.nitrogen * request.phosphorus) / 100
    logger.info(f"Prediction: nitrogen={request.nitrogen}, phosphorus={request.phosphorus}, yield={result}")
    return PredictionResponse(yield_prediction=result, confidence=0.92)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/ready")
def ready():
    return {"ready": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
