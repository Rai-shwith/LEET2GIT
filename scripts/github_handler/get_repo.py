from github import Github, AuthenticatedUser, Repository
from scripts.logging_config import logger

def get_repo(user: AuthenticatedUser, repo_name: str) -> Repository.Repository:
    """
    Get the repository
    """
    logger.info(f"Getting repository {repo_name}")
    try:
        repo = user.get_repo(repo_name)
        return repo
    except Exception as e:
        logger.error(f"Failed to get repository {repo_name}: {str(e)}")
        return None