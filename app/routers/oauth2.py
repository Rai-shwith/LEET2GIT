from fastapi import Depends, HTTPException,status,Request
import requests
from .logging_config import logger  
from ..schemas import GithubUser
from pydantic import ValidationError

GITHUB_API_URL = "https://api.github.com/user"

def get_current_user(request:Request)-> GithubUser:
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
        user = GithubUser(**response.json())
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve user")
    return user
