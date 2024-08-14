from pydantic import BaseModel
from datetime import datetime
from typing import Union

class ProblemDetails(BaseModel):
    questionTitle: str
    question: str
    link: str
    difficulty: str
    questionId: str
    titleSlug: str
    
class Solution(BaseModel):
    code_extension: str
    code: str
    
class Users(BaseModel):
    id : int
    user_name : str
    email : Union[str,None]
    github_id : int
    avatar_url : str
    folder_name : str
    created_at : datetime
    updated_at : datetime

class GithubUser(BaseModel):
    id: int  # GitHub user ID
    user_name: str
    email: str
    avatar_url: str

class GitHubAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str