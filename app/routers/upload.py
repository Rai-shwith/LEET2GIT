from fastapi import APIRouter, Depends, status,Request,WebSocket,WebSocketDisconnect
from scripts.github_handler.get_user_info import get_user_info
from scripts.output_content_creator import output_content_creator,output_content_creator_for_batch_upload
from scripts.leetcode_solutions_fetcher import leetcode_solution_fetcher
from scripts.github_handler.get_repo import get_repo
from scripts.github_handler.batch_upload import batch_upload_files
from scripts.github_handler.upload_file import upload_file,get_repo_readme_for_manual,get_repo_readme_bulk
from scripts.organize_leetcode_solutions import organize_leetcode_solutions
from ..database import get_db
from .oauth import get_current_user
from .. import schemas
from .logging_config import logger
from github import AuthenticatedUser
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import json


router  = APIRouter(prefix="/upload", tags=["upload"])

# @router.post("/api/",status_code=status.HTTP_201_CREATED,response_model=None)
async def create_uploads(request:Request,uploads: schemas.Uploads,db: AsyncSession):
# def create_uploads(request: Request,uploads: schemas.Uploads,current_user : schemas.Users):
    """
    This endpoint will create a new directory in github about the question and solution in the user's github repository
    This endpoint can be used to upload multiple problems together
    """
    file_structure = output_content_creator_for_batch_upload(uploads=uploads)
    github_user: AuthenticatedUser = await get_user_info(request=request)
    github_id = github_user.id
    current_user: schemas.Users = await get_current_user(github_id=github_id,db=db)
    logger.info(f"Creating the upload for the user: {current_user}")
    repo_name = current_user.repo_name
    repo = await get_repo(github_user,repo_name=repo_name)
    logger.info(f"Github user: {github_user}")
    repo_readme_content = await  get_repo_readme_for_manual(repo=repo,user_name=github_user.login,repo_name = current_user.repo_name,uploads=uploads)
    file_structure["README.md"]=repo_readme_content
    await batch_upload_files(repo=repo,file_structure=file_structure)
    logger.info("Upload Finished !!")
    

@router.post("/manual/",status_code=status.HTTP_201_CREATED)
async def manual_uploads(request:Request,uploads: schemas.Uploads,db: AsyncSession = Depends(get_db)):
    """
    This endpoint is for manual uploading """
    logger.info("Manual uploading ...")
    await create_uploads(request=request,uploads=uploads,db=db)

automatic_websocket_messages = [
    "Waiting for the data from the frontend",
    "Leetcode data received",
    "Processing the data",
    "Uploading the data to github",
    "Upload successful checkout your repository"
]

@router.websocket("/ws/automatic/")
async def automatic_uploads(websocket:WebSocket, db: AsyncSession = Depends(get_db)):
# async def automatic_uploads(websocket:WebSocket):
    message_index = 0
    """
    This endpoint is for automatic uploading """
    logger.info("Automatic uploading ...")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Data received from Automatic")
            data = json.loads(data)
            access_token = data["access_token"] 
            leetcode_credentials = data["leetcode_credentials"]
            await websocket.send_json(automatic_websocket_messages[0])
            message_index+=1
            try:
                raw_submissions = leetcode_solution_fetcher(leetcode_credentials.get("leetcodeAccess"))
            except Exception as e:
                # TODO: Handle the invalid token error in frontend
                logger.error(f"Error in fetching the leetcode submissions: {e}")
                await websocket.send_json({
                    "error":str(e)
                })
                return await websocket.close()
            # await asyncio.sleep(11)
            
            await websocket.send_json(automatic_websocket_messages[1])
            message_index+=1
            
            uploads: schemas.Uploads = await organize_leetcode_solutions(raw_solutions=raw_submissions)
            # await asyncio.sleep(22)
            
            await websocket.send_json(automatic_websocket_messages[2])
            message_index+=1
            # await create_uploads(request=request,uploads=uploads,db=db)
            
            file_structure = output_content_creator_for_batch_upload(uploads=uploads)
            # await asyncio.sleep(12)
            try:      
                github_user: AuthenticatedUser = await get_user_info(token=access_token)
                github_id = github_user.id
            except HTTPException:
                websocket.send_json({
                    "error":"Invalid Github Access Token"
                })
                websocket.close()
                
            await websocket.send_json(automatic_websocket_messages[3])
            message_index+=1
            
            current_user: schemas.Users = await get_current_user(github_id=github_id,db=db)
            logger.info(f"Creating the upload for the user: {current_user}")
            repo_name = current_user.repo_name
            repo = await get_repo(github_user,repo_name=repo_name)
            logger.info(f"Github user: {github_user}")
            repo_readme_content = await  get_repo_readme_bulk(repo=repo,user_name=github_user.login,repo_name = current_user.repo_name,uploads=uploads)
            file_structure["README.md"]=repo_readme_content
            await batch_upload_files(repo=repo,file_structure=file_structure)
            # await asyncio.sleep(133)
            
            # await websocket.send_text("Upload Finished !!")
            await websocket.send_json(automatic_websocket_messages[4])

            logger.info("Upload Finished !!")
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")