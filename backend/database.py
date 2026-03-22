from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.config import settings
from sqlalchemy.orm import DeclarativeBase

# echo=true логирует SQL запросы в консоль
engine = create_async_engine(settings.DB_URL, echo=False)

# ассинхронная фабрика сессий, expire_on_commit=True для актуальных данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)

# для всех ORM моделей
class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session_maker() as session:
        yield session