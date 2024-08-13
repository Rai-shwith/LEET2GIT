from pydantic import BaseModel
from datetime import datetime

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
    email : str
    password : str
    github_id : str
    avatar_url : str
    access_token : str
    folder_name : str
    created_at : datetime
    updated_at : datetime
