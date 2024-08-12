from github import Github
from scripts.logging_config import logger

def get_user_info(access_token):
    """
    Get the user information
    """
    logger.info("Getting user information")
    try:
        g = Github(access_token)
        user = g.get_user()
        return user
    except Exception as e:
        logger.error(f"Failed to get user information: {str(e)}")
        return None