from fastapi import APIRouter, HTTPException, status,Request
from fastapi.responses import RedirectResponse
from .logging_config import logger  
from ..utils import get_github_access_token
from .oauth import get_github_user,get_current_user



router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/github/callback")
async def get_github_callback(request:Request):
    logger.info("Github callback")
    code = request.query_params.get("code")
    if not code:
        logger.error("Invalid code")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code not found")
    logger.info("Code received")
    # Exchange the authorization code for an access token
    token_response = get_github_access_token(code)
    # Set the access token in an HTTP-only cookie
    response = RedirectResponse(url="/")
    response.set_cookie(
        key="access_token",
        value=token_response.access_token,
        httponly=True,  
        secure=True,    
        max_age=3600,   # for 1 hourdf
    )
    github_user = get_github_user(request,token=token_response.access_token)
    user = get_current_user(github_id=github_user.id)
    if user:
        response.set_cookie(
            key="registered",
            value="true",
            httponly=False,
            secure=True,
            max_age=3600,
        )
        logger.info("User already registered")
        return response
    logger.info("User authenticated and token set in cookie")
    return response
