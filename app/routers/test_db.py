from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "✅ Database connection successful!", "result": result.scalar()}
    except Exception as e:
        return {"status": "❌ Database connection failed.", "error": str(e)}
