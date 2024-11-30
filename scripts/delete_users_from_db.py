"WARNING: This script will delete all records in the users table."

from sqlalchemy.orm import Session
from app.models import Users
from app.database import get_db  # Import the get_db function from your database module

def delete_all_users():
    # Use get_db to obtain a database session
    db: Session = next(get_db())  # Extract the session generator
    try:
        # Delete all records in the users table
        db.query(Users).delete()
        db.commit()
        print("All users have been deleted.")
    except Exception as e:
        # Rollback in case of an error
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()  # Close the session manually, as we used `next()`

# Call the function
delete_all_users()
