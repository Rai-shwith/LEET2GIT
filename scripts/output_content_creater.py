import html
from scripts.logging_config import logger
from app.models import ProblemDetails,Solution


def output_content_creater(problem_detail:ProblemDetails,solution:Solution)->tuple[str,str,str,str]:
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
    read_me=f"""<h2><a href="{question_link}">{question_id}. {question_title}</a></h2><h3>{question_difficulty}</h3><hr>{question_body}"""    
    folder_name=f"{question_id:04}-{title_slug}"
    solution_file_name=f"{folder_name}.{solution.code_extension}"
    read_me_content=read_me
    logger.info("README.md file contents created successfully")
    return (read_me_content,solution_content,folder_name,solution_file_name)

  

