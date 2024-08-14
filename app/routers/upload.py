from fastapi import APIRouter, Depends, HTTPException, status,Request
from ..database import get_db
from .oauth2 import get_current_user
from sqlalchemy.orm import Session
from .. import models,schemas

router  = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/api/single",status_code=status.HTTP_201_CREATED)
def create_upload(upload: schemas.Upload, db: Session = Depends(get_db), user: schemas.Users = Depends(get_current_user)):
    """
    This endpoint will create a new directory about the question and solution in the user's github repository
    """
    return upload