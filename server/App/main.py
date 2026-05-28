import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routes.auth_router import router as auth_router
from app.routes.chat_router import router as chat_router
from app.routes.conversations_router import router as conversations_router

from app.databases.postgres_db import test_postgres_conn
from app.databases.redis_db import get_redis, close_redis
from app.databases.qdrant_db import get_qdrant, close_qdrant

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("EchoMind server starting...")

    # PostgreSQL
    if not test_postgres_conn():
        sys.exit(1)

    # Redis
    try:
        await get_redis()
        logger.info("Redis connected ✅")
    except Exception as e:
        logger.error(f"Redis connection failed ❌: {e}")
        sys.exit(1)

    # Qdrant
    try:
        await get_qdrant()
        logger.info("Qdrant connected ✅")
    except Exception as e:
        logger.error(f"Qdrant connection failed ❌: {e}")
        sys.exit(1)

    logger.info("EchoMind server ready ✅")

    yield

    logger.info("EchoMind server shutting down...")
    await close_redis()
    logger.info("Redis disconnected ✅")
    await close_qdrant()
    logger.info("Qdrant disconnected ✅")


app = FastAPI(
    title="EchoMind",
    description="AI powered assistant for meetings, audio, YouTube videos and Documents.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(conversations_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "EchoMind API is running"}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": "EchoMind",
    }
