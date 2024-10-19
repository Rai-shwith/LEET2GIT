from fastapi import APIRouter, Depends, HTTPException, status,Request
from fastapi.responses import RedirectResponse
from ..database import get_db
from .oauth import get_current_user,get_github_user,create_user
from sqlalchemy.orm import Session
from .. import models,schemas
from ..config import templates
from .logging_config import logger
from scripts.github_handler.create_repo import create_repo
from scripts.github_handler.get_repo import get_repo
from scripts.github_handler.get_user_info import get_user_info
from github import AuthenticatedUser

router = APIRouter(prefix="", tags=["users"])

@router.get("/register/api")
def register_user(request:Request,repo_name:str = "LeetCode",private:bool=True,new:bool=True, db: Session = Depends(get_db)):
    """
    This function will create a new user in the database
    """
    # return {"repo_name":repo_name,"private type":str(type(private)),"new type":str(type(new)),"private":private,"new":new}
    logger.info("Registering user")
    logger.info(f"Repo name: {repo_name}")
    github_user = get_github_user(request=request) # github user of pydantic type
    pygithub_user: AuthenticatedUser= get_user_info(request) # github user of pygithub type
    logger.info(f"Github user: {github_user}")
    if new:
        repo = create_repo(user=pygithub_user,repo_name=repo_name,private=private)
        logger.info(f"Repo {repo_name} already exists")
        if repo is None:
            logger.info(f"Repo {repo_name} already exists")
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Repository already exists")
    else:
        repo = get_repo(user=pygithub_user,repo_name=repo_name)
        if repo is None:
            logger.info(f"Repo {repo_name} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Repository not found")
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