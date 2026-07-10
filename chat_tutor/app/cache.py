import asyncio
import json
from redis.asyncio import Redis
from .config import settings

redis_cli: Redis = Redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

async def get_context(session_id: str) -> list[dict]:
    data = await redis_cli.get(f"context:{session_id}")
    return json.loads(data) if data else []

async def push_context(session_id: str, msg: dict):
    ctx = await get_context(session_id)
    ctx.append(msg)
    # keep only last N turns
    if len(ctx) > settings.CONTEXT_WINDOW:
        ctx = ctx[-settings.CONTEXT_WINDOW:]
    await redis_cli.set(f"context:{session_id}", json.dumps(ctx))

async def delete_context(session_id: str):
    await redis_cli.delete(f"context:{session_id}")
