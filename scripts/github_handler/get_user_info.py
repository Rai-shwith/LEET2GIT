from fastapi import Request
from github import Github,AuthenticatedUser,Auth
from scripts.logging_config import logger
from fastapi.concurrency import run_in_threadpool # to run the function in a thread

async def get_user_info(request:Request,token:str = None)->AuthenticatedUser:
    """
    Get the user information
    """
    if not token:
        token = request.cookies.get("access_token")
    logger.info("Getting user information")
    logger.info(f"Access token: {token}")
    try:
        auth = Auth.Token(token)
        logger.info(f"Auth object: {auth}")
        g = await run_in_threadpool(Github,auth) 
        logger.info("Github object created")
        logger.info(f"Github object: {g}")
        user = await run_in_threadpool(g.get_user)
        logger.info(f"User information: {user}")
        return user
    except Exception as e:
        logger.error(f"Failed to get user information: {str(e)}")
        return None