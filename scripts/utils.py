import os
from scripts.logging_config import logger

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
    