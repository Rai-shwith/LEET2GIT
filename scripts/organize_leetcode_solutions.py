from scripts.logging_config import logger
from app import schemas
from .problem_fetcher import get_problem_details

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
            problemDetails : schemas.ProblemDetails = await get_problem_details(title_slug=title_slug)
            solution : schemas.Solution = schemas.Solution(code=code,code_extension=code_extension)
            upload : schemas.Upload = schemas.Upload(question=problemDetails,solution=solution)
            uploads.append(upload)
            unique_recent_submissions[title_slug] = {"timestamp":timestamp,"index":len(uploads)-1}
        if title_slug in unique_recent_submissions and timestamp < unique_recent_submissions[title_slug]["timestamp"]:
            continue
        if title_slug in unique_recent_submissions and timestamp > unique_recent_submissions[title_slug]["timestamp"]:
            problemDetails : schemas.ProblemDetails = await get_problem_details(title_slug=title_slug)
            upload : schemas.Upload = schemas.Upload(question=problemDetails,solution=solution)
            uploads[unique_recent_submissions[title_slug]["index"]] = upload
            unique_recent_submissions[title_slug] = {"timestamp":timestamp,"index":len(uploads)-1}

    uploads : schemas.Uploads = schemas.Uploads(uploads=uploads)
    return uploads
            