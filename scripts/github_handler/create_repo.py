from scripts.logging_config import logger
from github import Github,AuthenticatedUser,Repository

def create_repo(user:AuthenticatedUser,repo_name:str,description:str="",private:bool=True)->Repository.Repository:
    logger.info(f"Creating repository {repo_name}")
    repo = user.create_repo(repo_name,description=description,private=private)
    logger.info(f"Repository {repo_name} created successfully")
    return repo

