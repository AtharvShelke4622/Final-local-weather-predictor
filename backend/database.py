from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from app_config import settings
from db_models import Base
from fastapi import Depends
import os
from urllib.parse import urlparse, parse_qs

# Get DATABASE_URL from environment
DATABASE_URL: str = os.environ.get("DATABASE_URL") or settings.DATABASE_URL or ""

# Convert postgresql:// to postgresql+asyncpg:// for async support
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Extract sslmode from URL and remove it (asyncpg uses connect_args)
parsed = urlparse(DATABASE_URL)
sslmode = "require"
if parsed.query:
    params = parse_qs(parsed.query)
    if "sslmode" in params:
        sslmode = params["sslmode"][0]
    # Remove sslmode from query
    clean_query = "&".join(k + "=" + v[0] for k, v in params.items() if k != "sslmode")
    DATABASE_URL = parsed._replace(query=clean_query).geturl()

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={"ssl": sslmode},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def ping_db():
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

async def get_session() -> AsyncSession:
    """Get database session dependency."""
    async with AsyncSessionLocal() as session:
        yield session
