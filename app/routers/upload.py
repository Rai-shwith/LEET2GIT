from fastapi import APIRouter, Depends, status,Request
from scripts.github_handler.get_user_info import get_user_info
from scripts.output_content_creater import output_content_creater
from scripts.leetcode_solutions_fetcher import leetcode_solution_fetcher
from scripts.github_handler.get_repo import get_repo
from scripts.github_handler.upload_file import upload_file,update_repo_readme
from scripts.organize_leetcode_solutions import organize_leetcode_solutions
from ..database import get_db
from .oauth import get_current_user
from .. import schemas
from .logging_config import logger
from github import AuthenticatedUser
import asyncio
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router  = APIRouter(prefix="/upload", tags=["upload"])

# @router.post("/api/",status_code=status.HTTP_201_CREATED,response_model=None)
async def create_uploads(request:Request,uploads: schemas.Uploads,db: AsyncSession):
# def create_uploads(request: Request,uploads: schemas.Uploads,current_user : schemas.Users):
    """
    This endpoint will create a new directory in github about the question and solution in the user's github repository
    This endpoint can be used to upload multiple problems together
    """
    github_user: AuthenticatedUser = await get_user_info(request=request)
    github_id = github_user.id
    current_user: schemas.Users = await get_current_user(github_id=github_id,db=db)
    logger.info(f"Creating the upload for the user: {current_user}")
    repo_name = current_user.repo_name
    repo = await get_repo(github_user,repo_name=repo_name)
    logger.info(f"Github user: {github_user}")
    for upload in uploads.uploads:
        (read_me_content,solution_content,folder_name,solution_file_name) = output_content_creater(problem_detail=upload.question,solution=upload.solution)
        logger.info(f"obtained the content for the files")
        await upload_file(repo,folder_name+"/README.md",read_me_content,"Added README.md")
        await upload_file(repo,folder_name+"/"+solution_file_name,solution_content,"Added solution file")
        await update_repo_readme(repo=repo,user_name=github_user.login,repo_name = current_user.repo_name,folder_name=folder_name,topic_tags=upload.question.topicTags)
    logger.info("Uploading Finished")
    

@router.post("/manual/",status_code=status.HTTP_201_CREATED)
async def manual_uploads(request:Request,uploads: schemas.Uploads,db: AsyncSession = Depends(get_db)):
    """
    This endpoint is for manual uploading """
    logger.info("Manual uploading ...")
    await create_uploads(request=request,uploads=uploads,db=db)
    

@router.post("/automatic/",status_code=status.HTTP_201_CREATED)  
async def automatic_uploads(request:Request,leetcode_credentials: schemas.LeetcodeCredentials,db: AsyncSession = Depends(get_db)):
    """
    This endpoint is for automatic uploading """
    logger.info("Automatic uploading ...")
    raw_submissions = leetcode_solution_fetcher(leetcode_credentials.leetcode_access_token,leetcode_credentials.csrftoken)
    uploads: schemas.Uploads = await organize_leetcode_solutions(raw_solutions=raw_submissions)
    await create_uploads(request=request,uploads=uploads,db=db)