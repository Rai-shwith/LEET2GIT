from fastapi import Depends, HTTPException,status,Request
import requests
from .logging_config import logger  
from .. import schemas,models
from pydantic import ValidationError
from ..database import get_db
from sqlalchemy.orm.session import Session
from typing import Union
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

GITHUB_API_URL = "https://api.github.com/user"

def get_github_user(request:Request,token:str = None) -> schemas.GithubUser:
    """
    This function will return the user from the githug API

    Args:
        request (fastapi.Request): This is the request object from the FastAPI route

    Returns:
        schemas.GithubUser: the schema object of the github user

    Raises:
        fastapi.HTTPException: If the token is invalid
    """
    logger.info("Verifying token")
    if not token:
        token = request.cookies.get("access_token")
    headers = {"Authorization": f"bearer {token}"}
    response = requests.get(GITHUB_API_URL, headers=headers)
    logger.info(f"Response: {response}")
    if response.status_code != 200:
        logger.error("Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token",headers={"WWW-Authenticate": "Bearer"})
    logger.info("Token verified")
    try:
        github_user = schemas.GithubUser(**response.json())
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve user")
    return github_user


def get_current_user(github_id:int)-> Union[schemas.Users,schemas.GithubUser]:
    """
    This function will return the current user from the database.
    If the user is not present in the database then it will return None
    """
    logger.info("Getting current user")
    db:Session=next(get_db())
    user = db.query(models.Users).filter(models.Users.github_id == github_id).first()
    return user
    # if not user:
    #     user = create_user(github_user,db=db)
    # else:
    #     user = schemas.Users.model_validate(user)
    # logger.info(f"Final_User to be returned: {user}")
    # return user


def create_user(github_user: schemas.GithubUser,repo_name:str,db:Session)-> schemas.Users:
    """
    Creates a new user in the database
    """
    logger.info("Creating a new user")
    try:
        new_user = models.Users(user_name=github_user.login,email=github_user.email,github_id=github_user.id,avatar_url=github_user.avatar_url,repo_name=repo_name)
        db.add(new_user)
        db.commit()
        logger.info(f"New user created: {new_user}")
    except (IntegrityError,UniqueViolation) as e:
        logger.error(f"Failed to create a new user: {str(e)}")
        return None
    db.refresh(new_user)
    logger.info(f"New user: {new_user}")
    return schemas.Users.model_validate(new_user)