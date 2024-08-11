import requests
from fastapi import HTTPException
import validators 
from logging_config import logger

def get_problem_details(url_or_question:str)->dict:
    """
    This function will fectch the information about mentioned problem from the api and returns the information in dictionary format
    """
    logger.info("Fetching problem details")
    if not validators.url(url_or_question): #Checks wheather the url is valid or not
        logger.info("Converting question name to url")
        url = url_maker(url_or_question)
    else:
        logger.info("Fetching data from the given url")
        url = url_or_question

    response = requests.get(url)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        if not data:
            logger.critical("Invalid URL")
            raise HTTPException(status_code = 404,detail="Invalid URL")
        logger.info("Data fetched successfully")
        return data
    else:
        logger.error("Failed to retrieve page")

def url_maker(question_name:str):
    """
        This fuction will convert name of the problem to proper url to fetch data
    """
    logger.info("Converting question name to url")
    url_template = "https://alfa-leetcode-api.onrender.com/select?titleSlug="
    question_name = question_name.strip()
    title_slug = question_name.replace(" ","-").replace("/","")#The string should be free of space and "/"
    url = url_template + title_slug
    logger.info(f"URL: {url}")
    return url