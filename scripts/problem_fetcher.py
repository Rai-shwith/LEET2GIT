import httpx
from fastapi import HTTPException
from .logging_config import logger
from app import schemas
from .utils import query_generator,create_title_slug_from_url,is_url


URL = "https://leetcode.com/graphql/"

async def get_problem_details(title_slug:str)->schemas.ProblemDetails:
    logger.info("Fetching problem details")
    if (is_url(title_slug=title_slug)):
        title_slug = create_title_slug_from_url(title_slug)
    query = query_generator(title_slug)
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(URL, json={"query": query})
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        if not data["data"]["question"]:
            logger.critical("Invalid URL")
            raise HTTPException(status_code = 404,detail="Invalid URL")
        logger.info("Data fetched successfully")
        logger.info(data)
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

