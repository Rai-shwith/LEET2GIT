from app import schemas
from scripts.logging_config import logger
from github import Github,Repository
from fastapi.concurrency import run_in_threadpool # to run the function in a thread
from scripts.README_templates.repo_README import get_repo_readme

async def upload_file(repo:Repository.Repository, file_name_with_path:str,content:str, commit_message:str):
    """
    Uploads a file to the particular directory in the repository
    """
    logger.info(f"Uploading {file_name_with_path} to the repository")
    try:
        contents_info = await run_in_threadpool(repo.get_contents,file_name_with_path)
        logger.info(f"{file_name_with_path} already exists. Updating the file")
        await run_in_threadpool(repo.update_file,contents_info.path, commit_message, content, contents_info.sha)
        logger.info(f"{file_name_with_path} updated successfully")
    except Exception as e:
        logger.info(f"Error: {str(e)}")
        logger.error(e)
        logger.info(f"{file_name_with_path}  Creating a new file")
        await run_in_threadpool(repo.create_file,file_name_with_path, commit_message, content)
        logger.info(f"{file_name_with_path} created successfully")
        
        
async def update_repo_readme(repo:Repository.Repository,user_name: str,repo_name : str,  folder_name : str, topic_tags:list[dict]):
    readme_file = repo.get_contents("README.md")
    logger.info(f"Updating the README.md file")
    readme_content = readme_file.decoded_content.decode("utf-8")
    readme_content = get_repo_readme(readme_content=readme_content,user_name=user_name,repo_name=repo_name,folder_name=folder_name,topic_tags=topic_tags)
    await upload_file(repo=repo,file_name_with_path="README.md",content=readme_content,commit_message="Updated README.md")

async def get_repo_readme_bulk(repo:Repository.Repository,user_name: str,repo_name : str, uploads:schemas.Uploads):
    topic_tag_dict = {} # To store the questions under the same topic tag
    for upload in uploads.uploads:
        topic_tags : list[dict] = upload.question.topicTags
        folder_name : str = f"{int(upload.question.questionId):04}-{upload.question.titleSlug}"
        if topic_tags == []:
            topic_tags = [{"name":"Miscellaneous"}]
        for tag in topic_tags:
            if tag.get('name') not in topic_tag_dict:
                topic_tag_dict[tag.get('name')] = []
            topic_tag_dict[tag.get('name')].append(folder_name)
            
    readme_start = "<!---LeetCode Topics Start-->\n"
    readme_end = "\n<!---LeetCode Topics End-->\nOrganized using <a href=\"https://github.com/Rai-shwith/LEET2GIT\" target=\"_blank\">LEET2GIT</a> to sync and structure the LeetCode solutions.\n"
    readme_center = "# LeetCode Topics\n"
    for tag in topic_tag_dict:
        folder_list = topic_tag_dict[tag]
        readme_center += f"## {tag}\n|  |\n| ------- |\n"
        for folder in folder_list:
            readme_center += f"| [{folder}](https://github.com/{user_name}/{repo_name}/tree/master/{folder}) |\n"
    
    readme_content = readme_start + readme_center + readme_end
    return readme_content