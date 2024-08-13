from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException,status
import requests
from .logging_config import logger  # Import the logger


auth_schema = OAuth2PasswordBearer(tokenUrl="token")

GITHUB_API_URL = "https://api.github.com/user"

def verity_github_token(token: str = Depends(auth_schema))-> dict:
    logger.info("Verifying token")
    headers = {"Authorization": f"token {token}"}
    response = requests.get(GITHUB_API_URL, headers=headers)
    logger.info(f"Response: {response}")
    if response.status_code != 200:
        logger.error("Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token",headers={"WWW-Authenticate": "Bearer"})
    logger.info("Token verified")
    return response.json()