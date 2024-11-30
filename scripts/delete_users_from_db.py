from sqlalchemy import text
from sqlalchemy.future import select
from app.models import Users  # Replace with your actual User model
from app.database import get_db  # Import the async get_db function

async def delete_all_users():
    async for db in get_db():  # Use the async generator to get a session
        try:
            # Execute the delete operation
            await db.execute(text("DELETE FROM users"))  # Use raw SQL query
            await db.commit()  # Commit the changes
            print("All users have been deleted.")
        except Exception as e:
            await db.rollback()  # Rollback in case of an error
            print(f"An error occurred: {e}")
        finally:
            await db.close()  # Ensure the session is properly closed

if __name__ == "__main__":
    import asyncio
    asyncio.run(delete_all_users())
