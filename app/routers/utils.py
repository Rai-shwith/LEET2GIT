from ..schemas import GitHubAccessTokenResponse
from ..config import settings
from fastapi import HTTPException, status
import requests
from .logging_config import logger

# Configuration variables (ideally from environment variables or a config file)
GITHUB_CLIENT_ID = settings.github_client_id
GITHUB_CLIENT_SECRET = settings.github_client_secret
GITHUB_TOKEN_URL = settings.github_token_url
GITHUB_REDIRECT_URI = settings.github_redirect_url



def get_github_access_token(code: str) -> GitHubAccessTokenResponse:
    """
    Exchange the authorization code for an access token.
    """
    response = requests.post(
        GITHUB_TOKEN_URL,
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        },
        headers={"Accept": "application/json"}
    )
    if response.status_code != 200:
        logger.error(f"Failed to get access token: {response.json()}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to retrieve access token"
        )
    return GitHubAccessTokenResponse(**response.json())