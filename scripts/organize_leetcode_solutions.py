from scripts.logging_config import logger
from app import schemas
from .problem_fetcher import get_problem_details


async def organize_leetcode_solutions(raw_solutions: dict)->schemas.Uploads:
    logger.info("Organizing Leetcode solutions ...")
    extension_map = {
    "Python3": "py",
    "Python": "py",
    "Pandas": "py",
    "Java": "java",
    "C": "c",
    "Cpp": "cpp",
    "Csharp": "cs",
    "Javascript": "js",
    "Typescript": "ts",
    "Ruby": "rb",
    "Swift": "swift",
    "Go": "go",
    "Kotlin": "kt",
    "Scala": "scala",
    "Rust": "rs",
    "Php": "php",
    "Mysql": "sql",
    "Bash": "sh",
    "Perl": "pl",
    "Haskell": "hs",
    "Dart": "dart",
    "Racket": "rkt",
    "Elixir": "ex",
    "Erlang": "erl",
    "Objective-C": "m",
    "Matlab": "m",  # Same extension as Objective-C
    "Fsharp": "fs",
    "Lua": "lua",
    "Groovy": "groovy",
    "Vb.net": "vb",
    "Fortran": "f90",
    "Pascal": "pas",
}

    submissions_dump = raw_solutions["submissions_dump"]
    print(submissions_dump)
    uploads = []
    for submission in submissions_dump:
        if submission["status_display"] == "Accepted":
            title_slug = submission["title_slug"]
            problemDetails : schemas.ProblemDetails = await get_problem_details(title_slug=title_slug)
            code_extension : str = extension_map[submission["lang_name"]]
            code : str = submission["code"]
            solution : schemas.Solution = schemas.Solution(code=code,code_extension=code_extension)
            upload : schemas.Upload = schemas.Upload(question=problemDetails,solution=solution)
            uploads.append(upload)
    uploads : schemas.Uploads = schemas.Uploads(uploads=uploads)
    return uploads
            