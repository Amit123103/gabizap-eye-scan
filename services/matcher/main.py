from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import redis
import json
from gabizap_common.config import BaseConfig
from gabizap_common.logger import setup_logger

logger = setup_logger("matcher-service")

class Config(BaseConfig):
    REDIS_URL: str

config = Config(SERVICE_NAME="matcher-service")
app = FastAPI(title="GABIZAP Distributed Matcher")

# Sync redis for simplicity in match loop, async is better for high scale
try:
    r = redis.from_url(config.REDIS_URL, decode_responses=True)
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    r = None

class MatchRequest(BaseModel):
    embedding: List[float]
    threshold: float = 0.85

@app.post("/register")
def register_template(user_id: str, embedding: List[float]):
    # Store embedding in Redis
    # Key: "template:{user_id}"
    if not r:
        raise HTTPException(status_code=503, detail="Matcher backend unavailable")
    
    key = f"template:{user_id}"
    r.set(key, json.dumps(embedding))
    return {"status": "registered", "user_id": user_id}

@app.post("/match")
def match_identity(req: MatchRequest):
    if not r:
        raise HTTPException(status_code=503, detail="Matcher backend unavailable")
    
    input_vec = np.array(req.embedding)
    input_norm = np.linalg.norm(input_vec)
    
    if input_norm == 0:
        raise HTTPException(status_code=400, detail="Invalid embedding vector")

    # SCAN for all templates (Naive Linear Search - O(N))
    # In production: Use RediSearch for vector similarity KNN
    best_score = -1.0
    best_user = None
    
    cursor = '0'
    while cursor != 0:
        cursor, keys = r.scan(cursor=cursor, match="template:*", count=100)
        if keys:
            values = r.mget(keys)
            for i, val in enumerate(values):
                if val:
                    stored_vec = np.array(json.loads(val))
                    stored_norm = np.linalg.norm(stored_vec)
                    
                    if stored_norm > 0:
                        # Cosine Similarity
                        score = np.dot(input_vec, stored_vec) / (input_norm * stored_norm)
                        
                        if score > best_score:
                            best_score = score
                            best_user = keys[i].split(":")[1]
    
    logger.info(f"Match result: Best={best_score}, User={best_user}")

    if best_score >= req.threshold:
        return {"match": True, "user_id": best_user, "score": float(best_score)}
    else:
        return {"match": False, "score": float(best_score)}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "matcher-service"}
