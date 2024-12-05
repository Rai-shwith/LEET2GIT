from fastapi import APIRouter, Depends, status,Request,WebSocket , WebSocketDisconnect
from scripts.github_handler.get_user_info import get_user_info
from scripts.output_content_creator import output_content_creator,output_content_creator_for_batch_upload
from scripts.leetcode_solutions_fetcher import leetcode_solution_fetcher
from scripts.github_handler.get_repo import get_repo
from scripts.github_handler.batch_upload import batch_upload_files
from scripts.github_handler.upload_file import upload_file,update_repo_readme,get_repo_readme_bulk
from scripts.organize_leetcode_solutions import organize_leetcode_solutions
from ..database import get_db
from .oauth import get_current_user
from .. import schemas
from .logging_config import logger
from github import AuthenticatedUser
import asyncio
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import json

router  = APIRouter(prefix="/upload", tags=["upload"])

# @router.post("/api/",status_code=status.HTTP_201_CREATED,response_model=None)
async def create_uploads(access_token:str,uploads: schemas.Uploads,db: AsyncSession,websocket:WebSocket):
# def create_uploads(request: Request,uploads: schemas.Uploads,current_user : schemas.Users):
    """
    This endpoint will create a new directory in github about the question and solution in the user's github repository
    This endpoint can be used to upload multiple problems together
    """
    file_structure = output_content_creator_for_batch_upload(uploads=uploads)
    github_user: AuthenticatedUser = await get_user_info(token=access_token)
    await websocket.send_text("User information received from Github")
    github_id = github_user.id
    current_user: schemas.Users = await get_current_user(github_id=github_id,db=db)
    logger.info(f"Creating the upload for the user: {current_user}")
    repo_name = current_user.repo_name
    repo = await get_repo(github_user,repo_name=repo_name)
    logger.info(f"Github user: {github_user}")
    # repo_readme_content = await  get_repo_readme_bulk(repo=repo,user_name=github_user.login,repo_name = current_user.repo_name,uploads=uploads)
    # file_structure["README.md"]=repo_readme_content
    await websocket.send_text("Uploading files to Github")
    await batch_upload_files(repo=repo,file_structure=file_structure)
    await websocket.send_text("Upload Finished !!")
    logger.info("Upload Finished !!")
    

@router.websocket("/ws/manual/")
async def manual_uploads(websocket:WebSocket, db: AsyncSession = Depends(get_db)):
    """
    This endpoint is for manual uploading """
    logger.info("Manual uploading ...")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Data received from Manual")
            data = json.loads(data)
            access_token = data["access_token"]
            uploads = schemas.Uploads(data["uploads"])
            await create_uploads(access_token=access_token,uploads=uploads,db=db,websocket=websocket)
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")
    

@router.websocket("/ws/automatic/")
async def automatic_uploads(websocket:WebSocket, db: AsyncSession = Depends(get_db)):
    """
    This endpoint is for automatic uploading """
    logger.info("Automatic uploading ...")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Data received from Manual")
            data = json.loads(data)
            access_token = data["access_token"]
            leetcode_credentials = data["leetcode_credentials"]
            await websocket.send_text("Fetching the leetcode submissions...")
            raw_submissions = leetcode_solution_fetcher(leetcode_credentials.get("LEETCODE_SESSION"))
            await websocket.send_text("Leetcode submissions fetched")
            uploads: schemas.Uploads = await organize_leetcode_solutions(raw_solutions=raw_submissions)
            await websocket.send_text("Leetcode solutions organized")
            # await create_uploads(request=request,uploads=uploads,db=db)
            file_structure = output_content_creator_for_batch_upload(uploads=uploads)
            github_user: AuthenticatedUser = await get_user_info(token=access_token)
            github_id = github_user.id
            await websocket.send_text("User information received from Github")
            current_user: schemas.Users = await get_current_user(github_id=github_id,db=db)
            logger.info(f"Creating the upload for the user: {current_user}")
            repo_name = current_user.repo_name
            repo = await get_repo(github_user,repo_name=repo_name)
            logger.info(f"Github user: {github_user}")
            repo_readme_content = await  get_repo_readme_bulk(repo=repo,user_name=github_user.login,repo_name = current_user.repo_name,uploads=uploads)
            file_structure["README.md"]=repo_readme_content
            await batch_upload_files(repo=repo,file_structure=file_structure)
            await websocket.send_text("Upload Finished !!")
            logger.info("Upload Finished !!")
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")
    
    