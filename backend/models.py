import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class TutorSession(Base):
    """
    One tutoring 'thread' with a student. This is what gives ChatTutor
    its context memory -- every message belongs to a session, and we
    replay the session's recent history back to the LLM on each ask.
    """
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=_uuid)
    student_name = Column(String, nullable=True)
    subject = Column(String, nullable=True)          # e.g. "algebra", "python"
    difficulty_level = Column(Float, default=1.0)     # used by adaptive learning
    created_at = Column(DateTime, default=_now)

    messages = relationship(
        "Message", back_populates="session",
        cascade="all, delete-orphan", order_by="Message.created_at"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    role = Column(String, nullable=False)   # "user" | "assistant"
    content = Column(Text, nullable=False)
    is_ambiguous = Column(Integer, default=0)  # 1 if flagged as an ambiguous query
    created_at = Column(DateTime, default=_now)

    session = relationship("TutorSession", back_populates="messages")
