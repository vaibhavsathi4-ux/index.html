from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, Session, Message

async def get_or_create_user(db: AsyncSession, user_id: str, email="") -> User:
    res = await db.execute(
        User.__table__.select().where(User.id == user_id)
    )
    user = res.scalar_one_or_none()
    if not user:
        user = User(id=user_id, email=email)
        db.add(user)
        await db.flush()
    return user

async def get_or_create_session(db: AsyncSession, user: User,
                                 subject: str | None, session_id: str | None) -> Session:
    if session_id:
        res = await db.execute(Session.__table__.select().where(Session.id == session_id))
        session = res.scalar_one_or_none()
        if session:
            return session
    session = Session(user_id=user.id, subject=subject)
    db.add(session)
    await db.flush()
    return session

async def add_message(db: AsyncSession, session: Session,
                      role: str, content: str, tokens=0, metadata=None):
    msg = Message(session_id=session.id, role=role,
                  content=content,
                  tokens_used=tokens,
                  metadata=metadata or {})
    db.add(msg)
    await db.flush()
    return msg