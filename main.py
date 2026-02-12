from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

app = FastAPI(title="GABIZAP API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models
class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str
    full_name: str = "Admin User"

# Simple demo authentication (no bcrypt needed)
DEMO_USERS = {
    "admin@gabizap.io": {
        "email": "admin@gabizap.io",
        "password": "admin123",  # In production, use hashed passwords
        "full_name": "Admin User"
    }
}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/")
async def root():
    return {
        "message": "GABIZAP API - Global AI Biometric Identity Platform",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "auth": "/auth/token"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "GABIZAP Backend"
    }

@app.post("/auth/token", response_model=Token)
async def login(credentials: LoginRequest):
    """
    Authenticate user and return JWT token
    """
    user = DEMO_USERS.get(credentials.email)
    
    if not user or user["password"] != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": credentials.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/api/user/me", response_model=User)
async def get_current_user():
    """
    Get current user information
    """
    return User(
        email="admin@gabizap.io",
        full_name="Admin User"
    )

@app.get("/api/stats")
async def get_stats():
    """
    Get system statistics
    """
    return {
        "active_sessions": 1248,
        "threat_level": "ELEVATED",
        "biometric_match_rate": 99.9,
        "blocked_ips": 42,
        "uptime": "99.99%"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
