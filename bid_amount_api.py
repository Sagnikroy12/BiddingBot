from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import numpy as np
import joblib  # or use pickle if your model was saved with pickle

# Load your trained ML model (replace with your actual model file)
model = joblib.load("bid_predictor_model.pkl")  # or .sav, .joblib, etc.

app = FastAPI()

class BidRequest(BaseModel):
    destination: Any
    spi: float
    freight: float

@app.post("/predict-bid/")
def predict_bid(data: BidRequest):
    # Preprocess input as needed (e.g., encode destination if categorical)
    # Example: if destination is categorical, use one-hot or label encoding
    # Here, we assume destination is already numeric or encoded
    features = np.array([[data.destination, data.spi, data.freight]])
    bid_pred = model.predict(features)
    return {"bid": float(bid_pred[0])}