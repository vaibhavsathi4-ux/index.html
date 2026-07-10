import pytest
from unittest.mock import AsyncMock, patch


# ---------------------------------------------------------
# Conversation Memory
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.chat_completion", new_callable=AsyncMock)
async def test_chat_memory(

    mock_llm,

    client,

    auth_headers,

):

    mock_llm.return_value = (

        "The derivative of sin(x) is cos(x).",

        15,

        100,

    )

    payload = {

        "user_id": "student",

        "subject": "math",

        "message": "Derivative of sin(x)?",

    }

    response = await client.post(

        "/ask",

        json=payload,

        headers=auth_headers,

    )

    assert response.status_code == 200

    session = response.json()["session_id"]

    mock_llm.return_value = (

        "The derivative of cos(x) is -sin(x).",

        20,

        110,

    )

    payload["session_id"] = session

    payload["message"] = "What about cos(x)?"

    response = await client.post(

        "/ask",

        json=payload,

        headers=auth_headers,

    )

    assert response.status_code == 200

    body = response.json()

    assert "answer" in body


# ---------------------------------------------------------
# Multiple Messages
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.chat_completion", new_callable=AsyncMock)
async def test_multiple_questions(

    mock_llm,

    client,

    auth_headers,

):

    mock_llm.return_value = (

        "Python is a programming language.",

        20,

        120,

    )

    for i in range(5):

        payload = {

            "user_id": "abc",

            "message": f"Question {i}",

            "subject": "python",

        }

        response = await client.post(

            "/ask",

            json=payload,

            headers=auth_headers,

        )

        assert response.status_code == 200


# ---------------------------------------------------------
# Empty Message
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_empty_message(

    client,

    auth_headers,

):

    payload = {

        "user_id": "abc",

        "message": "",

    }

    response = await client.post(

        "/ask",

        json=payload,

        headers=auth_headers,

    )

    assert response.status_code in (400, 422)


# ---------------------------------------------------------
# Missing User
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_missing_user(

    client,

    auth_headers,

):

    payload = {

        "message": "Hello",

    }

    response = await client.post(

        "/ask",

        json=payload,

        headers=auth_headers,

    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Conversation History
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.chat_completion", new_callable=AsyncMock)
async def test_history(

    mock_llm,

    client,

    auth_headers,

):

    mock_llm.return_value = (

        "History received.",

        10,

        90,

    )

    payload = {

        "user_id": "history",

        "message": "Explain loops",

        "history": [

            {

                "role": "user",

                "content": "Hello"

            },

            {

                "role": "assistant",

                "content": "Hi"

            }

        ]

    }

    response = await client.post(

        "/ask",

        json=payload,

        headers=auth_headers,

    )

    assert response.status_code == 200


# ---------------------------------------------------------
# Unicode Support
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.chat_completion", new_callable=AsyncMock)
async def test_unicode(

    mock_llm,

    client,

    auth_headers,

):

    mock_llm.return_value = (

        "नमस्ते",

        5,

        50,

    )

    payload = {

        "user_id": "india",

        "message": "नमस्ते",

    }

    response = await client.post(

        "/ask",

        json=payload,

        headers=auth_headers,

    )

    assert response.status_code == 200


# ---------------------------------------------------------
# Emoji
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.chat_completion", new_callable=AsyncMock)
async def test_emoji(

    mock_llm,

    client,

    auth_headers,

):

    mock_llm.return_value = (

        "😊",

        3,

        40,

    )

    payload = {

        "user_id": "emoji",

        "message": "🙂",

    }

    response = await client.post(

        "/ask",

        json=payload,

        headers=auth_headers,

    )

    assert response.status_code == 200


# ---------------------------------------------------------
# Long Conversation
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.chat_completion", new_callable=AsyncMock)
async def test_long_chat(

    mock_llm,

    client,

    auth_headers,

):

    mock_llm.return_value = (

        "ok",

        1,

        1,

    )

    session = None

    for i in range(20):

        payload = {

            "user_id": "user",

            "message": f"Question {i}",

            "session_id": session,

        }

        response = await client.post(

            "/ask",

            json=payload,

            headers=auth_headers,

        )

        assert response.status_code == 200

        session = response.json()["session_id"]