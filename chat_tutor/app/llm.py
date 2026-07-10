import os
import openai

from .config import settings

if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY

async def chat_completion(messages: list[dict]) -> tuple[str, int, float]:
    """
    Return (answer, tokens_used, latency)
    """
    import time
    start = time.perf_counter()
    response = await openai.ChatCompletion.acreate(
        model=settings.OPENAI_MODEL,
        messages=messages,
        max_tokens=settings.MAX_TOKENS,
        temperature=0.5,
        stream=False,
        seed=42,
    )
    latency = int((time.perf_counter() - start) * 1000)
    answer = response.choices[0].message.content.strip()
    usage = response.usage
    tokens = usage.total_tokens if usage else 0
    return answer, tokens, latency
