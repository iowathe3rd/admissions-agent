from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .models import Base
from .config import settings

# Use database URL from settings
DATABASE_URL = settings.DATABASE_URL

# Create async engine with proper configuration
async_engine = create_async_engine(
    DATABASE_URL, 
    echo=settings.DB_ECHO,  # Only enable echo in development
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
    pool_size=5,         # Default pool size
    max_overflow=10      # Maximum additional connections
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def init_db():
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        # In a real app, you would use Alembic for migrations.
        # For this MVP, we'll create tables directly.
        await conn.run_sync(Base.metadata.create_all)

# Alias for consistency
init_database = init_db

async def get_db():
    """Dependency for FastAPI to provide database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
