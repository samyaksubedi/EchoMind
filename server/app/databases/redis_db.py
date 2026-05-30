import redis.asyncio as redis
from app.config import settings

client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global client

    if client is None:
        client = redis.from_url(
            settings.get_redis_url,
            encoding="utf-8",
            decode_responses=True,  # returns strings instead of bytes
        )

    return client


async def close_redis():
    global client

    if client:
        await client.aclose()
        client = None
