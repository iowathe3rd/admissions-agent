from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .models import Base

DATABASE_URL = "sqlite+aiosqlite:///./admissions.db"

async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def init_db():
    async with async_engine.begin() as conn:
        # In a real app, you would use Alembic for migrations.
        # For this MVP, we'll create tables directly.
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
