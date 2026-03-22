from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.settings import settings

engine = create_async_engine(
    settings.db.url,
    echo=settings.db.echo,
    pool_size=5,
    max_overflow=10
)

async_session = async_sessionmaker(engine, expire_on_commit=False)
