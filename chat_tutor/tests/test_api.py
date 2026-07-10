import pytest
from unittest.mock import AsyncMock, patch


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_root(client):

    response = await client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["app"] == "ChatTutor"


# ---------------------------------------------------------
# Health Endpoint
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_health(client):

    response = await client.get("/health")

    assert response.status_code == 200


# ---------------------------------------------------------
# Ask Endpoint Success
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.chat_completion", new_callable=AsyncMock)
async def test_ask_success(
    mock_llm,
    client,
    auth_headers,
    ask_payload,
):

    mock_llm.return_value = (

        "Decorators wrap another function.",

        25,

        120,

    )

    response = await client.post(

        "/ask",

        json=ask_payload,

        headers=auth_headers,

    )

    assert response.status_code == 200

    body = response.json()

    assert body["answer"] == "Decorators wrap another function."

    assert body["tokens_used"] == 25

    assert body["latency_ms"] == 120


# ---------------------------------------------------------
# Missing JWT
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_missing_token(client, ask_payload):

    response = await client.post(

        "/ask",

        json=ask_payload,

    )

    assert response.status_code == 401


# ---------------------------------------------------------
# Invalid JWT
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_invalid_token(client, ask_payload):

    headers = {

        "Authorization": "Bearer invalid"

    }

    response = await client.post(

        "/ask",

        json=ask_payload,

        headers=headers,

    )

    assert response.status_code == 401


# ---------------------------------------------------------
# Empty Body
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_empty_body(client, auth_headers):

    response = await client.post(

        "/ask",

        json={},

        headers=auth_headers,

    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Invalid Request
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_invalid_request(client, auth_headers):

    payload = {

        "message": 123,

        "user_id": None,

    }

    response = await client.post(

        "/ask",

        json=payload,

        headers=auth_headers,

    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Large Prompt
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.chat_completion", new_callable=AsyncMock)
async def test_large_prompt(

    mock_llm,

    client,

    auth_headers,

):

    mock_llm.return_value = (

        "Large prompt handled.",

        300,

        200,

    )

    payload = {

        "user_id": "user1",

        "subject": "python",

        "message": "A" * 10000,

    }

    response = await client.post(

        "/ask",

        json=payload,

        headers=auth_headers,

    )

    assert response.status_code in (200, 413)


# ---------------------------------------------------------
# OpenAI Failure
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.chat_completion", new_callable=AsyncMock)
async def test_openai_error(

    mock_llm,

    client,

    auth_headers,

    ask_payload,

):

    mock_llm.side_effect = Exception("OpenAI Error")

    response = await client.post(

        "/ask",

        json=ask_payload,

        headers=auth_headers,

    )

    assert response.status_code >= 400


# ---------------------------------------------------------
# Wrong HTTP Method
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_method_not_allowed(client):

    response = await client.get("/ask")

    assert response.status_code == 405