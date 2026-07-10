import pytest
from unittest.mock import AsyncMock, patch

from app.llm import chat_completion


# ---------------------------------------------------------
# Basic AI Response
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.client.chat.completions.create", new_callable=AsyncMock)
async def test_ai_response(mock_create):

    mock_response = AsyncMock()

    mock_response.choices = [
        AsyncMock(
            message=AsyncMock(
                content="Python is a programming language."
            )
        )
    ]

    mock_response.usage.total_tokens = 20

    mock_create.return_value = mock_response

    answer, tokens, latency = await chat_completion(
        [
            {
                "role": "user",
                "content": "What is Python?"
            }
        ]
    )

    assert answer == "Python is a programming language."
    assert tokens == 20
    assert latency >= 0


# ---------------------------------------------------------
# Empty Prompt
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_empty_prompt():

    with pytest.raises(Exception):

        await chat_completion([])


# ---------------------------------------------------------
# OpenAI Exception
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.client.chat.completions.create", new_callable=AsyncMock)
async def test_openai_failure(mock_create):

    mock_create.side_effect = Exception("OpenAI Error")

    with pytest.raises(Exception):

        await chat_completion(
            [
                {
                    "role": "user",
                    "content": "Hello"
                }
            ]
        )


# ---------------------------------------------------------
# Large Prompt
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.client.chat.completions.create", new_callable=AsyncMock)
async def test_large_prompt(mock_create):

    response = AsyncMock()

    response.choices = [
        AsyncMock(
            message=AsyncMock(
                content="OK"
            )
        )
    ]

    response.usage.total_tokens = 500

    mock_create.return_value = response

    answer, tokens, latency = await chat_completion(
        [
            {
                "role": "user",
                "content": "A" * 10000
            }
        ]
    )

    assert answer == "OK"


# ---------------------------------------------------------
# Unicode
# ---------------------------------------------------------

@pytest.mark.asyncio
@patch("app.llm.client.chat.completions.create", new_callable=AsyncMock)
async def test_unicode(mock_create):

    response = AsyncMock()

    response.choices = [
        AsyncMock(
            message=AsyncMock(
                content="नमस्ते"
            )
        )
    ]

    response.usage.total_tokens = 5

    mock_create.return_value = response

    answer, _, _ = await chat_completion(
        [
            {
                "role": "user",
                "content": "नमस्ते"
            }
        ]
    )

    assert answer == "नमस्ते"