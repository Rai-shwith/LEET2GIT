import requests
from fastapi import HTTPException
from .logging_config import logger
from app import schemas
from .utils import query_generator

URL = "https://leetcode.com/graphql/"

def get_problem_details(title_slug:str)->schemas.ProblemDetails:
    logger.info("Fetching problem details")
    query = query_generator(title_slug)
    response = requests.post(URL, json={'query': query})
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        if not data:
            logger.critical("Invalid URL")
            raise HTTPException(status_code = 404,detail="Invalid URL")
        logger.info("Data fetched successfully")
        problem = data['data']['question']
        question_details = {
        "questionId": problem["questionId"],
        "questionFrontendId": problem["questionFrontendId"],
        "questionTitle": problem["title"],
        "question": problem["content"],
        "link": f"https://leetcode.com/problems/{problem['titleSlug']}",
        "difficulty": problem["difficulty"],
        "topicTags": problem["topicTags"],
        "titleSlug": problem["titleSlug"]
    }
        question_details = schemas.ProblemDetails(**question_details)
        return question_details
    else:
        logger.error("Failed to retrieve page")
        raise HTTPException(status_code = 404,detail="Failed to retrieve question details")

