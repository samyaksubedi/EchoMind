from qdrant_client import AsyncQdrantClient
from app.config import settings

client: AsyncQdrantClient | None = None


async def get_qdrant() -> AsyncQdrantClient:
    global client

    if client is None:
        client = AsyncQdrantClient(url=settings.get_qdrant_url)

    return client


async def close_qdrant():
    global client

    if client:
        await client.close()
        client = None
