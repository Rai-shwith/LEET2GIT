import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from app.config import settings
import ssl

async def test_async_db_connection():
    try:
        # Build the connection string
        SQL_ALCHEMY_DATABASE_URL = (
            f"{settings.database_protocol}+asyncpg://{settings.database_username}:"
            f"{settings.database_password}@{settings.database_host}:"
            f"{settings.database_port}/{settings.database_name}"
        )
        
        # Create SSL context
        ssl_context = ssl.create_default_context(cafile=settings.sslrootcert)
        
        # Initialize the async engine
        engine = create_async_engine(
            SQL_ALCHEMY_DATABASE_URL,
            connect_args={"ssl": ssl_context}
        )
        
        # Test the connection with an async session
        async with AsyncSession(engine) as session:
            result = await session.execute(select(1))
            print("✅ Successfully connected to the database (async)! Result:", result.scalar())

    except Exception as e:
        print("❌ Failed to connect to the database (async).")
        print("Error:", e)

    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_async_db_connection())

# Run this and let me know what happens! 🚀