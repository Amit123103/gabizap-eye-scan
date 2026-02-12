from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
import httpx
from gabizap_common.logger import setup_logger

logger = setup_logger("api-gateway")

class ZeroTrustMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, auth_url: str, risk_url: str):
        super().__init__(app)
        self.auth_url = auth_url
        self.risk_url = risk_url

    async def dispatch(self, request: Request, call_next):
        # Skip for public endpoints
        if request.url.path in ["/health", "/metrics", "/auth/token", "/auth/users/"]:
            return await call_next(request)
            
        # 1. Identity Verification (Authentication)
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response("Missing Authorization Header", status_code=401)
            
        # In a real gateway, we might validate the JWT signature locally to save latency
        # But for Zero Trust, we might want to consult the Auth Service for revocation status (Session Validation)
        # For this demo, we assume the downstream service or a dedicated auth check handles it.
        # Let's add a "Risk Check" simulation here.
        
        # 2. Risk Assessment (Contextual Access Control)
        # We simulate extracting context
        # In production: extract IP, DeviceID, etc.
        
        # Mocking a call to Risk Engine would introduce latency on every request
        # Usually this is done asynchronously or cached.
        # We will log the "Zero Trust Check" event.
        
        logger.info(f"Zero Trust Policy Check: {request.client.host} -> {request.url.path}")
        
        # 3. Proceed
        response = await call_next(request)
        return response
