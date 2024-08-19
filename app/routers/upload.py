from fastapi import APIRouter, Depends, status,Request
from scripts.github_handler.get_user_info import get_user_info
from scripts.output_content_creater import output_content_creater
from scripts.github_handler.get_repo import get_repo
from scripts.github_handler.upload_file import upload_file
from .oauth import get_current_user
from .. import schemas
from .logging_config import logger
from github import AuthenticatedUser
import asyncio
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router  = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/api/",status_code=status.HTTP_201_CREATED,response_model=None)
async def create_uploads(request:Request,uploads: schemas.Uploads,db: AsyncSession = Depends(get_db)):
    """
    This endpoint will create a new directory about the question and solution in the user's github repository
    """
    github_user: AuthenticatedUser = await get_user_info(request.cookies.get("access_token"))
    github_id = github_user.id
    current_user: schemas.Users = get_current_user(github_id=github_id,db=db)
    logger.info(f"Creating the upload for the user: {current_user}")
    repo_name = current_user.repo_name
    repo = await get_repo(github_user,repo_name=repo_name)
    logger.info(f"Github user: {github_user}")
    for upload in uploads.uploads:
        (read_me_content,solution_content,folder_name,solution_file_name) = output_content_creater(problem_detail=upload.question,solution=upload.solution)
        logger.info(f"obtained the content for the files")
        await asyncio.gather(
        upload_file(repo,folder_name+"/README.md",read_me_content,"Added README.md"),
        upload_file(repo,folder_name+"/"+solution_file_name,solution_content,"Added solution file")
        )
    # return {read_me_content,solution_content,folder_name,solution_file_name}