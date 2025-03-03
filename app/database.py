from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from typing import AsyncGenerator
import ssl

SQL_ALCHEMY_DATABASE_URL = (
    f"{settings.database_protocol}+asyncpg://{settings.database_username}:"
    f"{settings.database_password}@{settings.database_host}:"
    f"{settings.database_port}/{settings.database_host.split('.')[0]}.{settings.database_name}" #?sslmode={settings.database_connection_parameter}
)

ssl_context = ssl.create_default_context(cafile=settings.sslrootcert)

#create asynchronous engine
engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL
    ,connect_args={"ssl":ssl_context}
    )

#create async session maker
AsyncSessionLocal=sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False)

Base=declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
