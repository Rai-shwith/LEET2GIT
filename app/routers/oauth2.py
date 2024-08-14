from fastapi import Depends, HTTPException,status,Request
import requests
from .logging_config import logger  
from .. import schemas,models
from pydantic import ValidationError
from ..database import get_db
from sqlalchemy.orm import Session

GITHUB_API_URL = "https://api.github.com/user"

def get_current_user(request:Request,db:Session=Depends(get_db))-> schemas.Users:
    logger.info("Verifying token")
    token = request.cookies.get("access_token")
    headers = {"Authorization": f"bearer {token}"}
    response = requests.get(GITHUB_API_URL, headers=headers)
    logger.info(f"Response: {response}")
    if response.status_code != 200:
        logger.error("Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token",headers={"WWW-Authenticate": "Bearer"})
    logger.info("Token verified")
    logger.info(f"User: {response.json()}")
    try:
        github_user = schemas.GithubUser(**response.json())
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve user")
    user = db.query(models.Users).filter(models.Users.github_id == github_user.id).first()
    if not user:
        user = create_user(github_user)
    else:
        user = schemas.Users.model_validate(user)
    return user


def create_user(github_user: schemas.GithubUser,db:Session = Depends(get_db))-> schemas.Users:
    try:
        new_user = models.Users(user_name=github_user.login,email=github_user.email,github_id=github_user.id,avatar_url=github_user.avatar_url)
        db.add(new_user)
        db.commit()
    except Exception as e:
        return {"message":"User already exists"}
    db.refresh(new_user)
    return schemas.Users.model_validate(new_user)