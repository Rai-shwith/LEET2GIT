from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status,Request
from ..database import get_db
from .oauth import get_current_user
from sqlalchemy.orm import Session
from .. import models,schemas
from scripts import problem_fetcher
from urllib.parse import unquote

router  = APIRouter(prefix="/post", tags=["post"])

@router.get("/api",status_code=status.HTTP_200_OK,response_model=schemas.ProblemDetails)
async def create_upload(question: Optional[str] = Query(...,description="LeetCode question URL or title")):
    """
    This function will get the question name and fetch the information about the problem and return the problem details
    """
    question = unquote(question) # decoding eg :example%2Fstring%2Fwith%2Fslashes to  example/string/with/slashes
    problem_detail = await problem_fetcher.get_problem_details(question)
    return problem_detail
