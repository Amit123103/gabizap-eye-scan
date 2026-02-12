from fastapi import FastAPI, Depends, HTTPException
from gabizap_common.config import BaseConfig
from gabizap_common.logger import setup_logger

logger = setup_logger("user-service")

class Config(BaseConfig):
    DATABASE_URL: str

config = Config(SERVICE_NAME="user-service")

app = FastAPI(title="GABIZAP User Service")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "user-service"}

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from . import models

# Database Setup
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id, 
        "email": user.email, 
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active
    }
