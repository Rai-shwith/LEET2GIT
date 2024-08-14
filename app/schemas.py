from pydantic import BaseModel,EmailStr
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
    email : Union[EmailStr,None]
    github_id : int
    avatar_url : str
    folder_name : str
    created_at : datetime
    updated_at : datetime
    class Config:
        orm_mode = True
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