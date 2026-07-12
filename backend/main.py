import logging

import openai
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session as DBSession

from database import Base, engine, get_db
from models import TutorSession, Message
from llm_service import ask_tutor, adjust_difficulty
from schemas import SessionCreate, SessionOut, AskRequest, AskResponse, MessageOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chattutor")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ChatTutor API",
    description="AI tutor backend with per-session context memory and adaptive difficulty.",
    version="0.1.0",
)

# Wide-open CORS for hackathon/dev use. Lock this down before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/sessions", response_model=list[SessionOut])
def list_sessions(db: DBSession = Depends(get_db)):
    return db.query(TutorSession).order_by(TutorSession.created_at.desc()).all()


@app.post("/session", response_model=SessionOut)
def create_session(payload: SessionCreate, db: DBSession = Depends(get_db)):
    session = TutorSession(student_name=payload.student_name, subject=payload.subject)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@app.get("/session/{session_id}", response_model=SessionOut)
def get_session(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(TutorSession).filter(TutorSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/session/{session_id}/history", response_model=list[MessageOut])
def get_history(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(TutorSession).filter(TutorSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.messages


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, db: DBSession = Depends(get_db)):
    session = db.query(TutorSession).filter(TutorSession.id == payload.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found. Create one via POST /session first.")

    try:
        answer, ambiguous = ask_tutor(
            history=session.messages,
            question=payload.question,
            subject=session.subject,
            difficulty_level=session.difficulty_level,
        )
    except openai.APIStatusError as e:
        logger.error("OpenAI API error: %s", e)
        raise HTTPException(status_code=502, detail="Tutor model is temporarily unavailable. Please retry.")
    except openai.APIConnectionError as e:
        logger.error("OpenAI connection error: %s", e)
        raise HTTPException(status_code=503, detail="Could not reach the tutor model service.")
    except (openai.OpenAIError, TypeError) as e:
        # Covers missing/invalid API key and other client-side config errors.
        logger.error("OpenAI client configuration error: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Tutor model is not configured correctly on the server (check OPENAI_API_KEY).",
        )

    # Persist both sides of the exchange so future turns have full context.
    user_msg = Message(session_id=session.id, role="user", content=payload.question, is_ambiguous=int(ambiguous))
    assistant_msg = Message(session_id=session.id, role="assistant", content=answer)
    db.add_all([user_msg, assistant_msg])

    session.difficulty_level = adjust_difficulty(session.difficulty_level, payload.question)
    db.commit()
    db.refresh(session)

    return AskResponse(
        session_id=session.id,
        answer=answer,
        is_ambiguous=ambiguous,
        difficulty_level=session.difficulty_level,
        history=session.messages,
    )


@app.delete("/session/{session_id}")
def delete_session(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(TutorSession).filter(TutorSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"deleted": session_id}
