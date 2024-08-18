from fastapi import APIRouter, Depends, HTTPException, status,Request
from fastapi.responses import RedirectResponse
from ..database import get_db
from .oauth import get_current_user,get_github_user,create_user
from sqlalchemy.orm import Session
from .. import models,schemas
from ..config import templates
from .logging_config import logger

router = APIRouter(prefix="", tags=["users"])

@router.get("/register/api")
def register_user(request:Request,repo_name:str = "LeetBode", db: Session = Depends(get_db)):
    """
    This function will create a new user in the database
    """
    logger.info("Registering user")
    logger.info(f"Repo name: {repo_name}")
    github_user = get_github_user(request)
    logger.info(f"Github user: {github_user}")
    user = create_user(github_user=github_user,repo_name=repo_name,db=db)
    logger.info(f"User: {user}")
    response = RedirectResponse(url="/",status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="registered",
        value="true",
        httponly=False,
        secure=True,
        max_age=3600,
    )
    logger.info("User registered")
    return response