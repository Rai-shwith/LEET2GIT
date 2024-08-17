from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Union

    
class Users(BaseModel):
    id : int
    user_name : str
    email : Union[EmailStr,None]
    github_id : int
    avatar_url : str
    repo_name : str
    created_at : datetime
    updated_at : datetime
    class Config:
        from_attributes = True  # Enable validation from ORM attributes

class GithubUser(BaseModel):
    id: int  # GitHub user ID
    login: str # GitHub username
    email: Union[EmailStr, None]
    avatar_url: str

class GitHubAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class ProblemDetails(BaseModel):
    questionTitle: str
    question: str
    link: str
    difficulty: str
    questionId: str
    titleSlug: str
    topicTags: list[dict]
    
class Solution(BaseModel):
    code_extension: str
    code: str
    
class Upload(BaseModel):
    question: ProblemDetails
    solution: Solution
    
class Uploads(BaseModel):
    uploads: list[Upload]