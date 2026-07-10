from fastapi import APIRouter, Depends, HTTPException
from .schemas import AskRequest, AskResponse
from .deps import get_user_id, get_db, get_context, push_context
from .llm import chat_completion
from .crud import get_or_create_user, get_or_create_session, add_message
import uuid
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/ask", response_model=AskResponse)
@limiter.limit(f"{settings.RATE_LIMIT}/minute")
async def ask(payload: AskRequest,
              user_id: str = Depends(get_user_id),
              db = Depends(get_db)):
    # 1. User
    user = await get_or_create_user(db, user_id, email="")
    # 2. Session
    session = await get_or_create_session(db, user, payload.subject, payload.session_id)
    # 3. Build context
    context = await get_context(session.id)
    if payload.history:
        # Merge external history but keep token limits
        for m in payload.history:
            if len(context) >= settings.CONTEXT_WINDOW:
                context = context[-settings.CONTEXT_WINDOW:]
            context.append(m.dict())
    # Add current user message
    context.append({"role":"user", "content":payload.message})
    # 4. LLM
    answer, tokens, latency = await chat_completion(context)
    # 5. Persist messages
    await add_message(db, session, role="user", content=payload.message,
                      tokens=tokens, metadata={})
    await add_message(db, session, role="assistant",
                      content=answer, tokens=tokens, metadata={})
    await db.commit()
    # 6. Cache new context
    await push_context(session.id, {"role":"assistant","content":answer})
    return AskResponse(
        session_id=session.id,
        answer=answer,
        tokens_used=tokens,
        latency_ms=latency,
        metadata={"source":"llm"}
    )
