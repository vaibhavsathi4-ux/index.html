import pytest
from unittest.mock import AsyncMock, patch

from app.cache import (
    get_context,
    push_context,
    delete_context,
)

# -------------------------------------------------------
# Empty Cache
# -------------------------------------------------------

@pytest.mark.asyncio
@patch("app.cache.redis_cli")
async def test_empty_cache(redis):

    redis.get = AsyncMock(return_value=None)

    result = await get_context("abc")

    assert result == []


# -------------------------------------------------------
# Push Context
# -------------------------------------------------------

@pytest.mark.asyncio
@patch("app.cache.redis_cli")
async def test_push_context(redis):

    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock()

    await push_context(
        "session1",
        {
            "role": "user",
            "content": "Hello",
        },
    )

    redis.set.assert_called_once()


# -------------------------------------------------------
# Existing Context
# -------------------------------------------------------

@pytest.mark.asyncio
@patch("app.cache.redis_cli")
async def test_existing_context(redis):

    redis.get = AsyncMock(
        return_value='[{"role":"user","content":"Hi"}]'
    )

    result = await get_context("session")

    assert len(result) == 1

    assert result[0]["content"] == "Hi"


# -------------------------------------------------------
# Delete Cache
# -------------------------------------------------------

@pytest.mark.asyncio
@patch("app.cache.redis_cli")
async def test_delete_context(redis):

    redis.delete = AsyncMock()

    await delete_context("abc")

    redis.delete.assert_called_once()


# -------------------------------------------------------
# Redis Failure
# -------------------------------------------------------

@pytest.mark.asyncio
@patch("app.cache.redis_cli")
async def test_redis_failure(redis):

    redis.get.side_effect = Exception("Redis Down")

    with pytest.raises(Exception):

        await get_context("session")


# -------------------------------------------------------
# Long Conversation
# -------------------------------------------------------

@pytest.mark.asyncio
@patch("app.cache.redis_cli")
async def test_large_context(redis):

    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock()

    for i in range(50):

        await push_context(
            "session",
            {
                "role": "user",
                "content": f"Question {i}",
            },
        )

    assert redis.set.call_count == 50


# -------------------------------------------------------
# Unicode Cache
# -------------------------------------------------------

@pytest.mark.asyncio
@patch("app.cache.redis_cli")
async def test_unicode(redis):

    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock()

    await push_context(
        "unicode",
        {
            "role": "user",
            "content": "नमस्ते 😊",
        },
    )

    redis.set.assert_called_once()


# -------------------------------------------------------
# Cache Retrieval
# -------------------------------------------------------

@pytest.mark.asyncio
@patch("app.cache.redis_cli")
async def test_retrieve(redis):

    redis.get = AsyncMock(
        return_value='[{"role":"assistant","content":"Hello"}]'
    )

    result = await get_context("retrieve")

    assert result[0]["role"] == "assistant"


# -------------------------------------------------------
# Multiple Deletes
# -------------------------------------------------------

@pytest.mark.asyncio
@patch("app.cache.redis_cli")
async def test_multiple_delete(redis):

    redis.delete = AsyncMock()

    for i in range(5):

        await delete_context(f"session{i}")

    assert redis.delete.call_count == 5