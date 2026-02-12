from fastapi import FastAPI, UploadFile, File, HTTPException
from gabizap_common.config import BaseConfig
from gabizap_common.logger import setup_logger
from .model import IrisModel
import numpy as np

logger = setup_logger("iris-engine")

class Config(BaseConfig):
    MODEL_PATH: str = "models/iris_v1.h5"

config = Config(SERVICE_NAME="iris-engine")
model = IrisModel(config.MODEL_PATH)

app = FastAPI(title="GABIZAP Iris Engine")

@app.post("/embed")
async def create_embedding(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        embedding = model.get_embedding(contents)
        return {"embedding": embedding.tolist(), "version": "v1"}
    except Exception as e:
        logger.error(f"Error processing iris: {e}")
        raise HTTPException(status_code=500, detail="Processing failed")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "iris-engine"}
