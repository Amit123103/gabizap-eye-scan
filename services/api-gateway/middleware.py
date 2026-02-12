from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import redis.asyncio as redis
import time
from gabizap_common.logger import setup_logger

logger = setup_logger("api-gateway")

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, redis_url: str, limit: int = 100, window: int = 60):
        super().__init__(app)
        self.redis = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next):
        # Allow health checks without limiting
        if request.url.path == "/health":
            return await call_next(request)

        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        try:
            current = await self.redis.get(key)
            if current and int(current) >= self.limit:
                logger.warning(f"Rate limit exceeded for {client_ip}")
                return Response("Too Many Requests", status_code=429)
            
            async with self.redis.pipeline() as pipe:
                await pipe.incr(key)
                if not current:
                    await pipe.expire(key, self.window)
                await pipe.execute()
                
        except Exception as e:
            logger.error(f"Redis error in rate limiter: {e}")
            # Fail open if Redis is down, or closed? Secure systems fail closed.
            # For availability, we might fail open, but for "Defense Grade", fail closed.
            # Let's fail open for now to avoid locking out legitimate users during transient redis faults, 
            # but log heavily.
            pass

        response = await call_next(request)
        return response
