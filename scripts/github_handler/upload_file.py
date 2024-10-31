from scripts.logging_config import logger
from github import Github,Repository
from fastapi.concurrency import run_in_threadpool # to run the function in a thread
from scripts.README_templates.repo_README import get_repo_readme

async def upload_file(repo:Repository.Repository, file_name_with_path:str,content:str, commit_message:str):
    """
    Uploads a file to the perticular directory in the repository
    """
    logger.info(f"Uploading {file_name_with_path} to the repository")
    try:
        contents_info = await run_in_threadpool(repo.get_contents,file_name_with_path)
        logger.info(f"{file_name_with_path} already exists. Updating the file")
        await run_in_threadpool(repo.update_file,contents_info.path, commit_message, content, contents_info.sha)
        logger.info(f"{file_name_with_path} updated successfully")
    except:
        logger.info(f"{file_name_with_path}  Creating a new file")
        await run_in_threadpool(repo.create_file,file_name_with_path, commit_message, content)
        logger.info(f"{file_name_with_path} created successfully")
        
        
async def update_repo_readme(repo:Repository.Repository,user_name: str,repo_name : str,  folder_name : str, topic_tags:list[dict]):
    readme_file = repo.get_contents("README.md")
    logger.info(f"Updating the README.md file")
    readme_content = readme_file.decoded_content.decode("utf-8")
    readme_content = get_repo_readme(readme_content=readme_content,user_name=user_name,repo_name=repo_name,folder_name=folder_name,topic_tags=topic_tags)
    upload_file(repo=repo,file_name_with_path="README.md",content=readme_content,commit_message="Updated README.md")
