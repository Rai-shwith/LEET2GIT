from fastapi import APIRouter, Depends, HTTPException, status,Request
from ..database import get_db
from .oauth import get_current_user
from sqlalchemy.orm import Session
from .. import models,schemas
from scripts import problem_fetcher

router  = APIRouter(prefix="/post", tags=["post"])

@router.get("/api/{question}",status_code=status.HTTP_200_OK,response_model=schemas.ProblemDetails)
def create_upload(question:str):
    """
    This function will get the question name and fetch the information about the problem and return the problem details
    """
    problem_detail = problem_fetcher.get_problem_details(question)
    return problem_detail
