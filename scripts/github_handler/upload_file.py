from scripts.logging_config import logger
from github import Github,Repository

def upload_file(repo:Repository.Repository, file_name_with_path:str,content:str, commit_message:str):
    """
    Uploads a file to the perticular directory in the repository
    """
    logger.info(f"Uploading {file_name_with_path} to the repository")
    try:
        contents_info = repo.get_contents(file_name_with_path)
        logger.info(f"{file_name_with_path} already exists. Updating the file")
        repo.update_file(contents_info.path, commit_message, content, contents_info.sha)
        logger.info(f"{file_name_with_path} updated successfully")
    except:
        logger.info(f"{file_name_with_path}  Creating a new file")
        repo.create_file(file_name_with_path, commit_message, content)
        logger.info(f"{file_name_with_path} created successfully")