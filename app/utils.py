from .schemas import GitHubAccessTokenResponse
from .config import settings
from fastapi import HTTPException, status
import httpx
from .routers.logging_config import logger
from pydantic import ValidationError
from .security import encrypt_token

# Configuration variables (ideally from environment variables or a config file)
GITHUB_CLIENT_ID = settings.github_client_id
GITHUB_CLIENT_SECRET = settings.github_client_secret
GITHUB_TOKEN_URL = settings.github_token_url
GITHUB_REDIRECT_URI = settings.github_redirect_url



async def get_github_access_token(code: str) -> GitHubAccessTokenResponse:
    """
    Exchange the authorization code for an access token.
    """
    logger.info("Exchanging authorization code for access token")
    data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        }
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
        GITHUB_TOKEN_URL,
        data= data,
        headers={"Accept": "application/json"},
    )
    logger.info(f"Response: {response.json()}")
    if response.status_code != 200:
        logger.error(f"Failed to get access token: {response.json()}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to retrieve access token"
        )
    logger.info("Access token retrieved")
    data = response.json()
    try:
        access_token_response = GitHubAccessTokenResponse(
            access_token=encrypt_token(data["access_token"]),
            token_type=data["token_type"],
        ) 
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to retrieve access token"
        )
    return access_token_response