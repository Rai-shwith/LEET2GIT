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
    def __repr__(self):
        return f"<Users id={self.id} user_name='{self.user_name}' github_id={self.github_id}>"

    def __str__(self):
        return self.__repr__()

class GithubUser(BaseModel):
    id: int  # GitHub user ID
    login: str # GitHub username
    email: Union[EmailStr, None]
    avatar_url: str
    def __repr__(self):
        return f"<GitHubUser id={self.id} login='{self.login}'>"

    def __str__(self):
        return self.__repr__()

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
    topicTags: list[dict | None]
    def __repr__(self):
        return f"<ProblemDetails questionTitle={self.questionTitle} questionId={self.questionId}>"
    def __str__(self):
        return self.__repr__()
    
class Solution(BaseModel):
    code_extension: str
    code: str
    
class Upload(BaseModel):
    question: Union[ProblemDetails,None]
    solution: Solution
    
class Uploads(BaseModel):
    uploads: list[Upload]
    
class LeetcodeCredentials(BaseModel):
    leetcode_access_token: str