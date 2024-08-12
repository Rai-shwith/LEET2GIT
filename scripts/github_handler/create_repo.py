from scripts.logging_config import logger

def create_repo(user,repo_name:str,description:str="",private:bool=True):
    logger.info(f"Creating repository {repo_name}")
    repo = user.create_repo(repo_name,description=description,private=private)
    logger.info(f"Repository {repo_name} created successfully")
    return repo

