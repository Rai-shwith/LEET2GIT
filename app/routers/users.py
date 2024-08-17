from fastapi import APIRouter, Depends, HTTPException, status,Request
from ..database import get_db
from .oauth import get_current_user
from sqlalchemy.orm import Session
from .. import models,schemas
from ..config import templates

router = APIRouter(prefix="", tags=["users"])

@router.get("/profile")
def get_profile(request:Request,user: schemas.Users = Depends(get_current_user)):
    return templates.TemplateResponse("profile/index.html", {"request": request, "user": user})