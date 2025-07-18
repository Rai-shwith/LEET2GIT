from fastapi import FastAPI, Request,Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import users,auth,post,upload,test_db
from .config import templates
from .routers.oauth import get_github_user,get_current_user
from .routers.logging_config import logger
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .config import settings
# Add Jinja2 environment to FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://leetcode.com",
        "https://leet2git.ashwithrai.me"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/",response_model=None)
async def read_root(request: Request, db: AsyncSession = Depends(get_db)):
    logger.info("Root path")
    logger.info(f"Request: {request}")
    if not request.cookies.get("access_token"):
        logger.info("User not logged in")
        return templates.TemplateResponse("home/getStarted/index.html", {"request": request,"github_client_id":settings.github_client_id,"github_redirect_url":settings.github_redirect_url})
    logger.info("User logged in")
    github_user = await get_github_user(request)
    logger.info(f"Github user: {github_user}")
    if not request.cookies.get("registered"):
        logger.info("User not registered")
        return templates.TemplateResponse("home/logged/index.html", {"request": request,"user":github_user})
    logger.info("User registered")
    user = await get_current_user(github_id=github_user.id,db=db)
    logger.info(f"User: {user}")
    return templates.TemplateResponse("home/registered/index.html", {"request": request,"user":user,"domain":settings.domain})

app.include_router(users.router) # register the users in the database (sign up)
app.include_router(auth.router)  # authenticate the user (login)
app.include_router(post.router) # get the problem details
app.include_router(upload.router) # upload the problem details
app.include_router(test_db.router)
