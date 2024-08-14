from github import Github,AuthenticatedUser
from scripts.logging_config import logger

def get_user_info(access_token)->AuthenticatedUser:
    """
    Get the user information
    """
    logger.info("Getting user information")
    logger.info(f"Access token: {access_token}")
    try:
        g = Github(access_token)
        user = g.get_user()
        logger.info(f"User information: {user}")
        return user
    except Exception as e:
        logger.error(f"Failed to get user information: {str(e)}")
        return None