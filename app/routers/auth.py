from fastapi import APIRouter, Depends, HTTPException, status,Request
from fastapi.responses import RedirectResponse
from ..database import get_db
from .logging_config import logger  
from ..utils import get_github_access_token


router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/github/callback")
async def get_github_callback(request:Request):
    logger.info("Github callback")
    code = request.query_params.get("code")
    if not code:
        logger.error("Invalid code")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code not found")
    logger.info("Code received")
    logger.info(f"Code: {code}")
    # Exchange the authorization code for an access token
    token_response = get_github_access_token(code)
    # Set the access token in an HTTP-only cookie
    response = RedirectResponse(url="/profile")
    response.set_cookie(
        key="access_token",
        value=token_response.access_token,
        httponly=True,  
        secure=True,    
        max_age=86400,   # for 1 day
    )
    response.set_cookie(
        key="registered",
        value=False,
        httponly=True,  
        secure=True,    
        max_age=86400,   # for 1 day
    )
    
    logger.info("User authenticated and token set in cookie")
    return response
