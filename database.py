# database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql+asyncpg://postgres:password@0.0.0.0:5432/mydatabase"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Создаем фабрику сессий
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Функция для инициализации моделей
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
