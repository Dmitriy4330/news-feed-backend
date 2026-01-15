from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict  

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/newsfeed"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    DEBUG: bool = True
    

    model_config = ConfigDict(extra='allow', env_file=".env")

settings = Settings()
