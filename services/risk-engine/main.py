from fastapi import FastAPI, Body, BackgroundTasks
from pydantic import BaseModel
from gabizap_common.logger import setup_logger
import random
import numpy as np
import joblib
import os
from sklearn.ensemble import IsolationForest

logger = setup_logger("risk-engine")
app = FastAPI(title="GABIZAP Risk Engine")

MODEL_FILE = "risk_model.joblib"
model = None

# Mock training data for anomaly detection
def train_dummy_model():
    global model
    logger.info("Training initial risk model...")
    # Generate "normal" usage patterns
    # Features: [hour_of_day, device_trust_score, geo_distance, login_velocity]
    X_train = np.random.normal(loc=[12, 0.9, 10, 1], scale=[4, 0.1, 5, 0.5], size=(1000, 4))
    
    clf = IsolationForest(random_state=42, contamination=0.05)
    clf.fit(X_train)
    
    joblib.dump(clf, MODEL_FILE)
    model = clf
    logger.info("Risk model trained and saved.")

# Load model on startup
@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_FILE):
        model = joblib.load(MODEL_FILE)
    else:
        train_dummy_model()

class RiskContext(BaseModel):
    user_id: str
    hour: int
    device_trust: float # 0 to 1
    geo_dist: float     # km from last location
    velocity: float     # plugins per minute

@app.post("/score")
async def calculate_risk(context: RiskContext):
    if not model:
        # Fallback if model loading failed
        return {"risk_score": 50, "reason": "model_unavailable"}
    
    features = [[context.hour, context.device_trust, context.geo_dist, context.velocity]]
    
    # Predict anomaly: 1 for normal, -1 for anomaly
    prediction = model.predict(features)[0]
    score_raw = model.score_samples(features)[0]
    
    # Convert to 0-100 risk score
    # score_samples returns negative values, lower = more anomalous
    # Normal range roughly -0.5 to -0.8
    
    # Normalize heavily for demo
    # If prediction is -1 (anomaly), risk > 70
    
    if prediction == -1:
        risk_score = 85 + random.randint(0, 15)
        reason = "Behavioral Anomaly Detected"
    else:
        # Normal behavior
        risk_score = max(0, 100 * (0.5 - abs(score_raw))) # Crude normalization
        reason = "Normal Activity"
        
    logger.info(f"Risk analysis for {context.user_id}: {risk_score} ({reason})")
    
    action = "allow"
    if risk_score > 80:
        action = "block"
    elif risk_score > 50:
        action = "step_up"
        
    return {
        "risk_score": int(risk_score), 
        "action": action, 
        "anomaly": bool(prediction == -1)
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "risk-engine"}
