import pytest

from app.models import User, Session, Message
from app.crud import (
    get_or_create_user,
    get_or_create_session,
    add_message,
)

# -------------------------------------------------------
# Create User
# -------------------------------------------------------

@pytest.mark.asyncio
async def test_create_user(db):

    user = await get_or_create_user(
        db,
        user_id="student001",
        email="student@test.com",
    )

    await db.commit()

    assert user.id == "student001"
    assert user.email == "student@test.com"


# -------------------------------------------------------
# Existing User
# -------------------------------------------------------

@pytest.mark.asyncio
async def test_existing_user(db):

    user1 = await get_or_create_user(
        db,
        "existing",
        "existing@test.com",
    )

    await db.commit()

    user2 = await get_or_create_user(
        db,
        "existing",
        "existing@test.com",
    )

    assert user1.id == user2.id


# -------------------------------------------------------
# Create Session
# -------------------------------------------------------

@pytest.mark.asyncio
async def test_create_session(db):

    user = await get_or_create_user(
        db,
        "user1",
        "user@test.com",
    )

    session = await get_or_create_session(
        db,
        user,
        "python",
        None,
    )

    await db.commit()

    assert session.user_id == user.id
    assert session.subject == "python"


# -------------------------------------------------------
# Existing Session
# -------------------------------------------------------

@pytest.mark.asyncio
async def test_existing_session(db):

    user = await get_or_create_user(
        db,
        "user2",
        "user2@test.com",
    )

    session = await get_or_create_session(
        db,
        user,
        "math",
        None,
    )

    await db.commit()

    old_id = session.id

    same = await get_or_create_session(
        db,
        user,
        "math",
        old_id,
    )

    assert same.id == old_id


# -------------------------------------------------------
# Add Message
# -------------------------------------------------------

@pytest.mark.asyncio
async def test_add_message(db):

    user = await get_or_create_user(
        db,
        "user3",
        "user3@test.com",
    )

    session = await get_or_create_session(
        db,
        user,
        "python",
        None,
    )

    message = await add_message(
        db,
        session,
        role="user",
        content="Hello",
        tokens=10,
    )

    await db.commit()

    assert message.role == "user"
    assert message.tokens_used == 10


# -------------------------------------------------------
# Assistant Message
# -------------------------------------------------------

@pytest.mark.asyncio
async def test_assistant_message(db):

    user = await get_or_create_user(
        db,
        "assistant",
        "assistant@test.com",
    )

    session = await get_or_create_session(
        db,
        user,
        "AI",
        None,
    )

    msg = await add_message(
        db,
        session,
        role="assistant",
        content="Hello Student",
    )

    await db.commit()

    assert msg.role == "assistant"


# -------------------------------------------------------
# Rollback
# -------------------------------------------------------

@pytest.mark.asyncio
async def test_rollback(db):

    user = User(
        id="rollback",
        email="rollback@test.com",
    )

    db.add(user)

    await db.rollback()

    result = await db.get(User, "rollback")

    assert result is None


# -------------------------------------------------------
# Multiple Messages
# -------------------------------------------------------

@pytest.mark.asyncio
async def test_multiple_messages(db):

    user = await get_or_create_user(
        db,
        "multi",
        "multi@test.com",
    )

    session = await get_or_create_session(
        db,
        user,
        "python",
        None,
    )

    for i in range(10):

        await add_message(
            db,
            session,
            role="user",
            content=f"Message {i}",
        )

    await db.commit()

    assert True


# -------------------------------------------------------
# Delete User
# -------------------------------------------------------

@pytest.mark.asyncio
async def test_delete_user(db):

    user = await get_or_create_user(
        db,
        "delete",
        "delete@test.com",
    )

    await db.delete(user)

    await db.commit()

    result = await db.get(User, "delete")

    assert result is None