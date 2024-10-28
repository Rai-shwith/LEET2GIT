from github import Github, AuthenticatedUser, Repository, GithubException
from scripts.logging_config import logger

def get_repo(user: AuthenticatedUser, repo_name: str) -> Repository.Repository:
    """
    This function will get the repository with the given name
    return: Repository object if found else None
    """
    logger.info(f"Getting repository {repo_name}")
    try:
        repo = user.get_repo(repo_name)
        return repo
    except GithubException as e:
        if e.status == 404:
            logger.info(f"Repository {repo_name} not found")
            return None