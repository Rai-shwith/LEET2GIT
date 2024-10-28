from fastapi import APIRouter, Depends, HTTPException, status,Request
from scripts.github_handler.get_user_info import get_user_info
from scripts.output_content_creater import output_content_creater
from scripts.leetcode_solutions_fetcher import leetcode_solution_fetcher
from scripts.github_handler.get_repo import get_repo
from scripts.github_handler.create_repo import create_repo
from scripts.github_handler.upload_file import upload_file,update_repo_readme
from scripts.organize_leetcode_solutions import organize_leetcode_solutions
from ..database import get_db
from .oauth import get_current_user
from sqlalchemy.orm import Session
from .. import models,schemas
from .logging_config import logger
from github import AuthenticatedUser


router  = APIRouter(prefix="/upload", tags=["upload"])

def create_uploads(request: Request,uploads: schemas.Uploads,current_user : schemas.Users):
    """
    This endpoint will create a new directory in github about the question and solution in the user's github repository
    This endpoint can be used to upload multiple problems together
    """
    logger.info(f"Creating the upload for the user: {current_user}")
    repo_name = current_user.repo_name
    github_user: AuthenticatedUser = get_user_info(request=request)
    repo = get_repo(github_user,repo_name=repo_name)
    logger.info(f"Github user: {github_user}")
    for upload in uploads.uploads:
        (read_me_content,solution_content,folder_name,solution_file_name) = output_content_creater(problem_detail=upload.question,solution=upload.solution)
        logger.info(f"obtained the content for the files")
        # Upload Readme file 
        upload_file(repo,folder_name+"/README.md",read_me_content,"Added README.md")
        # Upload solution file
        upload_file(repo,folder_name+"/"+solution_file_name,solution_content,"Added solution file")
        # Update the README file by adding the folder name (new problem)
        update_repo_readme(repo=repo,user_name=github_user.login,repo_name = current_user.repo_name,folder_name=folder_name,topic_tags=upload.question.topicTags)

    logger.info("Uploading Finished")
    

@router.post("/mannual/",status_code=status.HTTP_201_CREATED)
def mannual_uploads(request:Request,uploads: schemas.Uploads,current_user: schemas.Users = Depends(get_current_user)):
    """
    This endpoint is for mannual uploading """
    logger.info("Mannual uploading ...")
    create_uploads(request=request,uploads=uploads,current_user=current_user)
    

@router.post("/automatic/",status_code=status.HTTP_201_CREATED)  
def automatic_uploads(request:Request,leetcode_credentials: schemas.LeetcodeCredentials,current_user: schemas.Users = Depends(get_current_user)):
    """
    This endpoint is for automatic uploading """
    logger.info("Automatic uploading ...")
    raw_submissions = leetcode_solution_fetcher(leetcode_credentials.leetcode_access_token,leetcode_credentials.csrftoken)
    uploads: schemas.Uploads = organize_leetcode_solutions(raw_solutions=raw_submissions)
    create_uploads(request=request,uploads=uploads,current_user=current_user)