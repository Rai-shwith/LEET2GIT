from scripts.logging_config import logger
from app import schemas
from .problem_fetcher import get_problem_details
import asyncio

def get_extension(language):
    extension_map = {
        "python3": "py",
        "python": "py",
        "pandas": "py",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "csharp": "cs",
        "javascript": "js",
        "typescript": "ts",
        "ruby": "rb",
        "swift": "swift",
        "go": "go",
        "kotlin": "kt",
        "scala": "scala",
        "rust": "rs",
        "php": "php",
        "mysql": "sql",
        "bash": "sh",
        "perl": "pl",
        "haskell": "hs",
        "dart": "dart",
        "racket": "rkt",
        "elixir": "ex",
        "erlang": "erl",
        "objective-c": "m",
        "matlab": "m",
        "fsharp": "fs",
        "lua": "lua",
        "groovy": "groovy",
        "vb.net": "vb",
        "fortran": "f90",
        "pascal": "pas",
        "julia": "jl",  # Newly added languages
        "prolog": "pl",
        "scheme": "scm",
        "cobol": "cbl",
        "solidity": "sol",
    }

    return extension_map.get(language.lower(), "txt")  # Default to txt if language not found


async def organize_leetcode_solutions(raw_solutions: dict)->schemas.Uploads:
    logger.info("Organizing Leetcode solutions ...")
    
    submissions_dump = raw_solutions["submissions_dump"]
    
    # unique_recent_submissions is for storing the most recent submission for each problem
    unique_recent_submissions = {}
    uploads = []
    
    tasks = []  # List to hold async tasks
    task_mapping = {}  # Map title_slug to the task index for updating results
    
    for submission in submissions_dump:
        # Only consider accepted submissions
        if submission["status_display"] != "Accepted":
            continue
        timestamp = submission["timestamp"]
        title_slug = submission["title_slug"]
        code_extension : str = get_extension(submission["lang_name"])
        code : str = submission["code"]
        solution : schemas.Solution = schemas.Solution(code=code,code_extension=code_extension)
        
        # if the submission is not in the unique_recent_submissions, add it directly 
        if title_slug not in unique_recent_submissions:
            
            # Schedule get_problem_details task
            task = asyncio.create_task(get_problem_details(title_slug=title_slug))
            tasks.append(task)
            task_mapping[title_slug] = len(tasks) - 1  # Map title_slug to task index
            
            upload : schemas.Upload = schemas.Upload(question=None,solution=solution)
            uploads.append(upload)
            unique_recent_submissions[title_slug] = {"timestamp":timestamp,"index":len(uploads)-1}
        if title_slug in unique_recent_submissions and timestamp < unique_recent_submissions[title_slug]["timestamp"]:
            continue
        if title_slug in unique_recent_submissions and timestamp > unique_recent_submissions[title_slug]["timestamp"]:
            unique_recent_submissions[title_slug]["timestamp"] = timestamp
            problemDetails : schemas.ProblemDetails = await get_problem_details(title_slug=title_slug)
            upload : schemas.Upload = schemas.Upload(question=None,solution=solution)
            uploads[unique_recent_submissions[title_slug]["index"]] = upload

    # Await all tasks and update uploads with fetched problem details
    problem_details_list = await asyncio.gather(*tasks)
    for title_slug, task_index in task_mapping.items():
        problem_details = problem_details_list[task_index]
        index = unique_recent_submissions[title_slug]["index"]
        uploads[index].question = problem_details
    
    uploads : schemas.Uploads = schemas.Uploads(uploads=uploads)
    import json
    with open("JUNK/temp123.json",'w') as f:
        f.write(json.dumps(uploads.model_dump()))
    return uploads
            