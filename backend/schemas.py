from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    student_name: Optional[str] = None
    subject: Optional[str] = None


class SessionOut(BaseModel):
    id: str
    student_name: Optional[str]
    subject: Optional[str]
    difficulty_level: float
    created_at: datetime

    class Config:
        from_attributes = True


class AskRequest(BaseModel):
    session_id: str
    question: str = Field(..., min_length=1)


class MessageOut(BaseModel):
    role: str
    content: str
    created_at: datetime
    is_ambiguous: bool = False

    class Config:
        from_attributes = True


class AskResponse(BaseModel):
    session_id: str
    answer: str
    is_ambiguous: bool
    difficulty_level: float
    history: List[MessageOut]
