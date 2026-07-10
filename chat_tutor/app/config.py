import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # DB
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    # Redis
    REDIS_URL: str = Field(..., env='REDIS_URL')
    # Auth
    JWT_SECRET: str = Field(..., env='JWT_SECRET')
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_SECONDS: int = 900  # 15 min
    # LLM
    OPENAI_API_KEY: str | None = Field(None, env='OPENAI_API_KEY')
    OPENAI_MODEL: str = "gpt-3.5-turbo-0125"
    # Limits
    CONTEXT_WINDOW: int = 10  # last N turns
    RATE_LIMIT: int = 30  # per minute
    MAX_TOKENS: int = 1024

settings = Settings()