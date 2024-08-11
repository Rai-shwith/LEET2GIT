import html
from scripts.utils import save_file
from scripts.logging_config import logger


def read_me_creater(problem_detail:dict)->None:
    """
    Reads the problem detail and creates a README.md file for the problem
    """
    # Read the problem detail
    logger.info("Creating README.md file")
    try:
        question_title = problem_detail["questionTitle"]
        question_body = html.unescape(problem_detail["question"])
        question_link = problem_detail["link"]
        question_difficulty = problem_detail["difficulty"]
        question_id = int(problem_detail["questionId"])
        title_slug = problem_detail["titleSlug"]
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return None
    read_me=f"""<h2><a href="{question_link}">{question_id}. {question_title}</a></h2><h3>{question_difficulty}</h3><hr>{question_body}"""
    folder_name=f"OUTPUT/{question_id:04}-{title_slug}"
    file_name="README.md"
    content=read_me
    save_file(folder_name=folder_name,file_name=file_name,content=content )
    logger.info("README.md file created successfully")

