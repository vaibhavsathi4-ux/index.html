from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Message(BaseModel):
    role: str = Field(..., regex="^(user|assistant)$")
    content: str
    timestamp: Optional[str] = None

class AskRequest(BaseModel):
    user_id: str
    message: str
    session_id: Optional[str] = None
    subject: Optional[str] = None
    history: Optional[List[Message]] = None

class AskResponse(BaseModel):
    session_id: str
    answer: str
    tokens_used: int
    latency_ms: int
    metadata: dict | None = None
