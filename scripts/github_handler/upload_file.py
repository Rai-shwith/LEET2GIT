from scripts.logging_config import logger
from github import Github,Repository

def upload_file(repo:Repository.Repository, file_name:str,content:str, commit_message:str):
    """
    Uploads a file to the repository
    """
    logger.info(f"Uploading {file_name} to the repository")
    try:
        contents_info = repo.get_contents(file_name)
        logger.info(f"{file_name} already exists. Updating the file")
        repo.update_file(contents_info.path, commit_message, content, contents_info.sha)
        logger.info(f"{file_name} updated successfully")
    except:
        logger.info(f"{file_name}  Creating a new file")
        repo.create_file(file_name, commit_message, content)
        logger.info(f"{file_name} created successfully")