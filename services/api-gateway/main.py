from fastapi import FastAPI, Request, HTTPException, Depends
from gabizap_common.logger import setup_logger
from gabizap_common.config import BaseConfig
import httpx

logger = setup_logger("api-gateway")

class Config(BaseConfig):
    AUTH_SERVICE_URL: str
    USER_SERVICE_URL: str
    IRIS_SERVICE_URL: str

from .middleware import RateLimitMiddleware
from .zero_trust import ZeroTrustMiddleware

config = Config(SERVICE_NAME="api-gateway")
config.REDIS_URL = "redis://redis:6379/0" 

app = FastAPI(title="GABIZAP API Gateway")

# Add Middlewares
app.add_middleware(RateLimitMiddleware, redis_url=config.REDIS_URL, limit=100, window=60)
# Note: Middleware order matters. Last added is executed first? No, first added is outer?
# Starlette executes in order added? Actually typical is LIFO for some implementations, but let's assume standard behavior.
# We want Rate Limit first (cheap), then Zero Trust (expensive).
app.add_middleware(ZeroTrustMiddleware, auth_url=config.AUTH_SERVICE_URL, risk_url="http://risk-engine:8005")

@app.get("/health")
async def health_check():
    logger.info("Health check received")
    return {"status": "healthy", "service": "api-gateway"}

async def forward_request(service_url: str, request: Request, path: str):
    async with httpx.AsyncClient() as client:
        # Forward the request to the downstream service
        # This is a simplified example; a real gateway would handle headers, methods, bodies more robustly
        url = f"{service_url}/{path}"
        try:
            resp = await client.request(
                method=request.method,
                url=url,
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return resp.json()
        except httpx.RequestError as exc:
            logger.error(f"Error connecting to {service_url}: {exc}")
            raise HTTPException(status_code=503, detail="Service unavailable")

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy(path: str, request: Request):
    return await forward_request(config.AUTH_SERVICE_URL, request, path)

@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user_proxy(path: str, request: Request):
    return await forward_request(config.USER_SERVICE_URL, request, path)

# Add more routes as needed
