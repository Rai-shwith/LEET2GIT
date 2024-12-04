import os
import sys
import pytest
from fastapi import Request,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import schemas
from app.routers.upload import create_uploads
from github import AuthenticatedUser,Repository  
from scripts.github_handler.get_user_info import get_user_info
from scripts.github_handler.get_repo import get_repo
from starlette.datastructures import Headers
from app.routers.oauth import get_current_user
from scripts.github_handler.get_repo import get_repo
from scripts.output_content_creator import output_content_creator
from app.routers.users import register_user
import json





# Add the root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
# Set up the token from environment variables
token = os.getenv("github_token")
scope = {
    "type": "http",
    "headers": Headers({"cookie": f"access_token={token}; registered=true"}).raw,
}
request = Request(scope=scope)  # Create a dummy request object
with open("JUNK/uploads.json", "r") as f:
    uploads_data = f.read()  # Read the content as a string
    uploads = schemas.Uploads.model_validate_json(uploads_data) 
with open("JUNK/output_content.json", "r") as f:
    output_content = json.load(f)
upload = uploads.uploads[0]



@pytest.mark.skip()
@pytest.mark.asyncio
async def test_get_user_info():
    user = await get_user_info(request=request, token=token)
    assert isinstance(user, AuthenticatedUser.AuthenticatedUser)

@pytest.mark.skip()
@pytest.mark.asyncio
async def test_get_current_user():
    async for db in get_db() :
        user = await get_user_info(request=request, token=token)
        current_user = await get_current_user(github_id=user.id,db=db)
    assert isinstance(current_user, schemas.Users)

@pytest.mark.skip() 
@pytest.mark.asyncio
async def test_get_repo():
    async for db in get_db() :
        github_user = await get_user_info(request=request, token=token)
        current_user = await get_current_user(github_id=github_user.id,db=db)
        repo_name = current_user.repo_name
        repo = await get_repo(github_user,repo_name=repo_name)
    assert isinstance(repo, Repository.Repository)

@pytest.mark.skip()
def test_output_content_creator():
    (read_me_content,solution_content,folder_name,solution_file_name) = output_content_creator(problem_detail=upload.question,solution=upload.solution)
    output = {
        "read_me_content": read_me_content,
        "solution_content": solution_content,
        "folder_name": folder_name,
        "solution_file_name": solution_file_name
    }
    assert output == output_content
    
pytest.mark.skip()
@pytest.mark.asyncio
async def test_create_uploads():
    async for db in get_db() :
        uploads.uploads.clear()
        uploads.uploads.extend([upload])
        await create_uploads(request=request,uploads=uploads,db=db)
    assert True
    
@pytest.mark.asyncio
async def test_register_user():
    a = await register_user(request=request,repo_name="LeetCode",private=True,new=True)
    assert(isinstance(a, AsyncSession))