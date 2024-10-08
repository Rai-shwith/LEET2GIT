from scripts.logging_config import logger
from github import Github,AuthenticatedUser,Repository
from .upload_file import upload_file

def create_repo(user:AuthenticatedUser,repo_name:str,description:str="",private:bool=True)->Repository.Repository:
    if description=="":
        description="Repository created by LEET2GIT for storing LeetCode solutions"
    logger.info(f"Creating repository {repo_name}")
    repo = user.create_repo(repo_name,description=description,private=private)
    logger.info(f"Repository {repo_name} created successfully")
    initial_read_me_content :str = "This repository is created by LEET2GIT for storing LeetCode solutions. Developed by <a href=\"https://github.com/Rai-shwith\">Rai-shwith</a>"
    upload_file(repo,"README.md",initial_read_me_content,f"Initial commit for {repo_name}")
    return repo

