from scripts.logging_config import logger
from fastapi import HTTPException
def query_generator(title_slug):
    title_slug = title_slug.replace(" ","-").replace("/","")#The string should be free of space and "/"
    
    query = f"""
    query {{
    question(titleSlug: "{title_slug}") {{
    questionId
    questionFrontendId
    title
    titleSlug
    content
    difficulty
    topicTags {{
    name
    slug
    translatedName
    }}
    }}
    }}
    """
    logger.info("Query generated")
    return query
    
    
def create_title_slug_from_url(url: str):
    """
    Extract the title slug from the url
    """
    logger.info("Extracting title slug from URL")
    start_index = url.find("problems/") + len("problems/")
    end_index = url.find("/", start_index) #The title slug ends with a "/"
    end_index = None if end_index == -1 else end_index #If the title slug is the last part of the URL that is if it doesn't have '/' at the end
    print(start_index,end_index);
    title_slug = url[start_index:end_index]
    logger.info("Title slug extracted from URL")
    return title_slug

def is_url(title_slug: str):
    """
    Validate the URL
    """
    logger.info("Validating URL")
    if "leetcode.com"  in title_slug:
        logger.info('Title Slug is URL')
        return True
    else:
        logger.info('Title Slug is not URL')
        return False