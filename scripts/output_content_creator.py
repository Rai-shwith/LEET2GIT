import html
from scripts.logging_config import logger
from app import schemas
from .README_templates.question_README import question_Read_me_constructor


def output_content_creator(problem_detail:schemas.ProblemDetails,solution:schemas.Solution)->tuple[str,str,str,str]:
    """
    Reads the problem detail and returns README.md file contents ,solution file contents  and folder name  for the problem
    """
    # Read the problem detail
    logger.info("Creating README.md file contents")
    
    try:
        question_title = problem_detail.questionTitle
        question_body = html.unescape(problem_detail.question)
        question_link = problem_detail.link
        question_difficulty = problem_detail.difficulty
        question_id = int(problem_detail.questionId)
        title_slug = problem_detail.titleSlug
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return None
    
      # Read the raw solution
    logger.info("Creating solution file")
    solution_content=solution.code
    logger.info("Solution file created successfully")
    read_me = question_Read_me_constructor(question_link,question_id,question_title,question_difficulty,question_body)
    folder_name=f"{question_id:04}-{title_slug}"
    solution_file_name=f"{folder_name}.{solution.code_extension}"
    read_me_content=read_me
    logger.info("README.md file contents created successfully")
    return (read_me_content,solution_content,folder_name,solution_file_name)

  
  
def output_content_creator_for_batch_upload(uploads: schemas.Uploads)->dict:
    """
    Description: This function generates proper structure for batch upload to github repository.

    Args:
        uploads (schemas.Uploads): The uploads object containing the list of uploads.

    Returns:
       file_structure: A dictionary representing files and their content. 
                        Example: {"path/to/file1.txt": "Content of file1", "path/to/file2.txt": "Content of file2"}
    """
    file_structure = {}
    for upload in uploads.uploads:
        (read_me_content,solution_content,folder_name,solution_file_name) = output_content_creator(problem_detail=upload.question,solution=upload.solution)
        file_structure[folder_name+"/README.md"] = read_me_content
        file_structure[folder_name+"/"+solution_file_name] = solution_content
    return file_structure
