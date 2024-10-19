from fastapi import APIRouter, Depends, HTTPException, status,Request
from ..database import get_db
from .oauth import get_current_user
from sqlalchemy.orm import Session
from .. import models,schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/api",status_code=status.HTTP_201_CREATED,response_model=schemas.Users)
def create_user(folder_name:str="LeetCode",db:Session = Depends(get_db),user: dict = Depends(get_current_user)):
    """
    Creates a new user in the database.

    Args:
        folder_name (str): The name of the folder to be created for the user. Defaults to "LeetCode".
        db (Session): The database session.
        user (dict): The user details obtained from the authentication process.

    Returns:
        schemas.Users: The newly created user object.

    Raises:
        HTTPException: If the user already exists in the database.
    """
    try:
        new_user = models.Users(user_name=user['login'],email=user['email'],github_id=user['id'],avatar_url=user['avatar_url'],folder_name=folder_name)
        db.add(new_user)
        db.commit()
    except Exception as e:
        return {"message":"User already exists"}
    db.refresh(new_user)
    return new_user


@router.get("/profile")
def get_profile(request:Request,user: schemas.Users = Depends(get_current_user)):
    return user