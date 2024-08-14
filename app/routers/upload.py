from fastapi import APIRouter, Depends, HTTPException, status,Request
from scripts.github_handler.get_user_info import get_user_info
from scripts.output_content_creater import output_content_creater
from ..database import get_db
from .oauth2 import get_current_user
from sqlalchemy.orm import Session
from .. import models,schemas
from .logging_config import logger
from github import AuthenticatedUser


router  = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/api/single",status_code=status.HTTP_201_CREATED)
def create_upload(request:Request,upload: schemas.Upload, db: Session = Depends(get_db), db_user: schemas.Users = Depends(get_current_user)):
    """
    This endpoint will create a new directory about the question and solution in the user's github repository
    """
    logger.info("Creating a new directory in the user's github repository")
    github_user: AuthenticatedUser = get_user_info(request.cookies.get("access_token"))
    logger.info(f"Github user: {github_user}")
    (read_me_content,solution_content,folder_name,solution_file_name) = output_content_creater(problem_detail=upload.question,solution=upload.solution)
    logger.info(f"obtained the content for the files")
    return github_user