from fastapi import Depends, HTTPException,status,Request
import requests
from .logging_config import logger  



GITHUB_API_URL = "https://api.github.com/user"

def get_current_user(request:Request)-> dict:
    logger.info("Verifying token")
    token = request.cookies.get("access_token")
    headers = {"Authorization": f"token {token}"}
    response = requests.get(GITHUB_API_URL, headers=headers)
    logger.info(f"Response: {response}")
    if response.status_code != 200:
        logger.error("Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token",headers={"WWW-Authenticate": "Bearer"})
    logger.info("Token verified")
    return response.json()

