from fastapi import FastAPI, Body
from pydantic import BaseModel
from datetime import datetime
from gabizap_common.logger import setup_logger

logger = setup_logger("audit-service")
app = FastAPI(title="GABIZAP Audit Service")

class AuditLog(BaseModel):
    service: str
    event_type: str
    user_id: str = None
    details: dict
    timestamp: str = None

@app.post("/log")
async def create_audit_log(log: AuditLog):
    if not log.timestamp:
        log.timestamp = datetime.utcnow().isoformat()
        
    logger.info(f"AUDIT_EVENT: {log.json()}")
    # In production: write to Audit Table (immutable append-only)
    return {"status": "recorded", "id": "evt_12345"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "audit-service"}
