from pydantic_settings import BaseSettings
from typing import Optional

class BaseConfig(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = False
    SERVICE_NAME: str
    
    # Database
    DATABASE_URL: Optional[str] = None
    
    # Redis
    REDIS_URL: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "unsafe_default_key_for_dev_only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        extra = "ignore"

class PostgresConfig(BaseConfig):
    pass

class RedisConfig(BaseConfig):
    pass
