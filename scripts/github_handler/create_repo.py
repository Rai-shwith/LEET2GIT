from scripts.logging_config import logger
from github import Github,AuthenticatedUser,Repository,GithubException
from .upload_file import upload_file
from fastapi.concurrency import run_in_threadpool # to run the function in a thread

async def create_repo(user:AuthenticatedUser,repo_name:str,description:str="",private:bool=True)->Repository.Repository:
    """
    This function will create a new repository with the given name ,description and privacy
    return: Repository object if created successfully else None
    """
    if description=="":
        description="Repository created by LEET2GIT for storing LeetCode solutions."
    logger.info(f"Creating repository {repo_name}")
    try:
        repo = await run_in_threadpool(user.create_repo,repo_name,description=description,private=private)
        logger.info(f"Repository {repo_name} created successfully")
        initial_read_me_content :str = "This repository is created by LEET2GIT for storing LeetCode solutions. Developed by <a href=\"https://github.com/Rai-shwith\">Rai-shwith</a>\n"
        await upload_file(repo,"README.md",initial_read_me_content,f"Initial commit for {repo_name}")
        return repo
    except GithubException as e:
        if e.status==422:
            logger.info(f"Repository {repo_name} already exists")
            return None

