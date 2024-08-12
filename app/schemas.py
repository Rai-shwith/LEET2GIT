from pydantic import BaseModel

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