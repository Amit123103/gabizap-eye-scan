from fastapi import FastAPI, Request
from gabizap_common.logger import setup_logger
import redis
import time

logger = setup_logger("honeypot")
app = FastAPI(title="Legacy Admin Panel - RESTRICTED")
r = redis.Redis(host='redis-master', port=6379, db=0)

BLACKLIST_PREFIX = "blacklisted_ip:"

@app.get("/admin/legacy_login")
@app.post("/admin/legacy_login")
async def fake_login(request: Request):
    """
    TRAP: This endpoint does not exist in the real app.
    Anyone touching this is a scanner or attacker.
    """
    client_ip = request.client.host
    logger.critical(f"🚨 HONEYPOT TRIGGERED by IP: {client_ip}")
    
    # 1. Immediate Blacklist (Active Defense)
    r.setex(f"{BLACKLIST_PREFIX}{client_ip}", 86400, "honeypot_trap") # 24h ban
    
    # 2. Deception - Return fake error to keep them guessing
    # Slow response to waste their time (Tarpit)
    time.sleep(2) 
    return {"error": "Invalid legacy credentials. Please use port 8080."}

@app.get("/config.php")
@app.get("/.env")
async def trap_scanners(request: Request):
    """Common vulnerability scanner targets."""
    return await fake_login(request)
