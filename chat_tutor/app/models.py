import uuid
import json
from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    preferences = Column(JSON, default=dict)
    sessions = relationship("Session", back_populates="owner")

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    subject = Column(String)
    started_at = Column(DateTime(timezone=True), default=func.now())
    ended_at = Column(DateTime(timezone=True))
    owner = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("sessions.id"))
    role = Column(String)  # user / assistant
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    tokens_used = Column(Integer, default=0)
    metadata = Column(JSON, default=dict)
    session = relationship("Session", back_populates="messages")
