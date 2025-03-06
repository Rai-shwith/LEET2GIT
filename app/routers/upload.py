from fastapi import APIRouter, Depends, status,Request,WebSocket,WebSocketDisconnect
from scripts.github_handler.get_user_info import get_user_info
from scripts.output_content_creator import output_content_creator,output_content_creator_for_batch_upload
from scripts.leetcode_solutions_fetcher import leetcode_solution_fetcher
from scripts.github_handler.get_repo import get_repo
from scripts.github_handler.batch_upload import batch_upload_files
from scripts.github_handler.upload_file import upload_file,get_repo_readme_for_manual,get_repo_readme_bulk
from scripts.organize_leetcode_solutions import organize_leetcode_solutions
from ..database import get_db
from .oauth import get_current_user
from .. import schemas
from .logging_config import logger
from github import AuthenticatedUser
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import json
import uuid


router  = APIRouter(prefix="/upload", tags=["upload"])

# @router.post("/api/",status_code=status.HTTP_201_CREATED,response_model=None)
async def create_uploads(request:Request,uploads: schemas.Uploads,db: AsyncSession):
# def create_uploads(request: Request,uploads: schemas.Uploads,current_user : schemas.Users):
    """
    This endpoint will create a new directory in github about the question and solution in the user's github repository
    This endpoint can be used to upload multiple problems together
    """
    file_structure = output_content_creator_for_batch_upload(uploads=uploads)
    github_user: AuthenticatedUser = await get_user_info(request=request)
    github_id = github_user.id
    current_user: schemas.Users = await get_current_user(github_id=github_id,db=db)
    logger.info(f"Creating the upload for the user: {current_user}")
    repo_name = current_user.repo_name
    repo = await get_repo(github_user,repo_name=repo_name)
    logger.info(f"Github user: {github_user}")
    repo_readme_content = await  get_repo_readme_for_manual(repo=repo,user_name=github_user.login,repo_name = current_user.repo_name,uploads=uploads)
    file_structure["README.md"]=repo_readme_content
    await batch_upload_files(repo=repo,file_structure=file_structure)
    logger.info("Upload Finished !!")
    

@router.post("/manual/",status_code=status.HTTP_201_CREATED)
async def manual_uploads(request:Request,uploads: schemas.Uploads,db: AsyncSession = Depends(get_db)):
    """
    This endpoint is for manual uploading """
    logger.info("Manual uploading ...")
    await create_uploads(request=request,uploads=uploads,db=db)

automatic_websocket_messages = [
    "Waiting for the data from the frontend",
    "Leetcode data received",
    "Processing the data",
    "Uploading the data to github",
    "Upload successful checkout your repository"
]

webSocketConnections = {}

@router.websocket("/ws/")
async def test(websocket:WebSocket):
    """
    This endpoint is for testing the websocket connection
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Data received from the frontend: {data}")
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")
        await websocket.close()

@router.websocket("/ws/automatic/")
async def automatic_initialization(websocket:WebSocket):
    """
    This endpoint is for initialization of automatic uploading 
    """
    id = uuid.uuid4()
    print(id)
    webSocketConnections[id] = websocket
    await websocket.accept()
    await websocket.send_json({
        "code":"const connection_id = '" + id +r"""'async function getProblemDetails(titleSlug) {const BASE_URL = "https://leetcode.com/graphql/";const query = queryGenerator(titleSlug);try {const response = await fetch(BASE_URL, {method: "POST",headers: { "Content-Type": "application/json" },body: JSON.stringify({ query }),});if (!response.ok) {console.error("Failed to retrieve page");throw new Error("Failed to retrieve question details");}const data = await response.json();if (!data || !data.data || !data.data.question) {console.error("Invalid URL");throw new Error("Invalid URL");}const problem = data.data.question;return {questionId: problem.questionId,questionFrontendId: problem.questionFrontendId,questionTitle: problem.title,question: problem.content,link: `https://leetcode.com/problems/${problem.titleSlug}`,difficulty: problem.difficulty,topicTags: problem.topicTags,titleSlug: problem.titleSlug,};} catch (error) {console.error(error.message);throw new Error(error.message);}}function queryGenerator(titleSlug) {titleSlug = titleSlug.replace(/ /g, "-").replace(/\//g, "");const query = `query { question(titleSlug: "${titleSlug}") { questionId questionFrontendId title titleSlug content difficulty topicTags { name slug translatedName } }}`;return query;}function getExtension(language) {const extensionMap = {python3: "py",python: "py",pandas: "py",java: "java",c: "c",cpp: "cpp",csharp: "cs",javascript: "js",typescript: "ts",ruby: "rb",swift: "swift",go: "go",kotlin: "kt",scala: "scala",rust: "rs",php: "php",mysql: "sql",bash: "sh",perl: "pl",haskell: "hs",dart: "dart",racket: "rkt",elixir: "ex",erlang: "erl","objective-c": "m",matlab: "m",fsharp: "fs",lua: "lua",groovy: "groovy","vb.net": "vb",fortran: "f90",pascal: "pas",julia: "jl",prolog: "pl",scheme: "scm",cobol: "cbl",solidity: "sol",};return extensionMap[language.toLowerCase()] || "txt";}async function organizeLeetcodeSolutions(rawSolutions) {console.log("Organizing Leetcode solutions...");const submissionsDump = rawSolutions.submissions_dump;const uniqueRecentSubmissions = {};const uploads = [];const tasks = [];const taskMapping = {};console.log("Starting Leetcode Question fetch.");for (const submission of submissionsDump) {if (submission.status_display !== "Accepted") continue;const { timestamp, title_slug, lang_name, code } = submission;const code_extension = getExtension(lang_name);const solution = { code, code_extension };if (!uniqueRecentSubmissions[title_slug]) {const task = getProblemDetails(title_slug);tasks.push(task);taskMapping[title_slug] = tasks.length - 1;uploads.push({ question: null, solution });uniqueRecentSubmissions[title_slug] = {timestamp,index: uploads.length - 1,};}if (uniqueRecentSubmissions[title_slug]?.timestamp < timestamp) {uniqueRecentSubmissions[title_slug].timestamp = timestamp;uploads[uniqueRecentSubmissions[title_slug].index] = {question: null,solution,};}}const problemDetailsList = await Promise.all(tasks);for (const [titleSlug, taskIndex] of Object.entries(taskMapping)) {const problemDetails = problemDetailsList[taskIndex];const index = uniqueRecentSubmissions[titleSlug].index;uploads[index].question = problemDetails;}return { uploads };}function sleep(ms) {return new Promise((resolve) => setTimeout(resolve, ms));}async function fetchSubmissions() {console.log("Starting Leetcode submission fetch");let offset = 0;let hasNext = true;let submissions = { submissions_dump: [] };while (hasNext) {try {const response = await fetch(`https://leetcode.com/api/submissions/?offset=${offset}`);if (!response.ok) {throw new Error("HTTP error! status: ${response.status}");}const data = await response.json();submissions.submissions_dump.push(...(data.submissions_dump || []));offset += 20;hasNext = data.has_next;await sleep(500);} catch (error) {console.error("Error:", error);break;}} ;const socket = new WebSocket(`ws://localhost:8000/upload/ws/automatic/${connection_id}`);socket.onopen = () => {console.log("Socket connected");organizeLeetcodeSolutions(submissions).then((data) => {console.log("Sending data to the server...");socket.send(JSON.stringify(data));}).catch((error) => {console.error("Error:", error);});};socket.onmessage = (event) => {console.log(event.message);};}fetchSubmissions();""",
        'message':automatic_websocket_messages[0]
    })
    
    
@router.websocket("/ws/automatic/{connection_id}")
async def automatic_uploads(websocket:WebSocket,connection_id:str, db: AsyncSession = Depends(get_db)):
# async def automatic_uploads(websocket:WebSocket):
    if connection_id not in webSocketConnections:
        await websocket.send_text("Invalid Connection ID")
        return await websocket.close()
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        logger.info(f"Data received from Automatic")
        
        await websocket.send_text("Data received by leet2git.")
        
        data = json.loads(data)
        uploads: schemas.Uploads = schemas.Uploads(uploads=data["uploads"])
        
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")
        await websocket.close()
    
    message_index = 0
    """
    This endpoint is for automatic uploading """
    logger.info("Automatic uploading ...")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Data received from Automatic")
            data = json.loads(data)
            uploads: schemas.Uploads = schemas.Uploads(uploads=data["uploads"])
            id = data["id"]
                
            leetcode_credentials = data["leetcode_credentials"]
            await websocket.send_json(automatic_websocket_messages[0])
            message_index+=1
            try:
                raw_submissions = leetcode_solution_fetcher(leetcode_credentials.get("leetcodeAccess"))
            except Exception as e:
                # TODO: Handle the invalid token error in frontend
                logger.error(f"Error in fetching the leetcode submissions: {e}")
                await websocket.send_json({
                    "error":str(e)
                })
                return await websocket.close()
            # await asyncio.sleep(11)
            
            await websocket.send_json(automatic_websocket_messages[1])
            message_index+=1
            
            # await asyncio.sleep(22)
            
            await websocket.send_json(automatic_websocket_messages[2])
            message_index+=1
            # await create_uploads(request=request,uploads=uploads,db=db)
            
            file_structure = output_content_creator_for_batch_upload(uploads=uploads)
            # await asyncio.sleep(12)
            try:      
                github_user: AuthenticatedUser = await get_user_info(token=access_token)
                github_id = github_user.id
            except HTTPException:
                websocket.send_json({
                    "error":"Invalid Github Access Token"
                })
                websocket.close()
                
            await websocket.send_json(automatic_websocket_messages[3])
            message_index+=1
            
            current_user: schemas.Users = await get_current_user(github_id=github_id,db=db)
            logger.info(f"Creating the upload for the user: {current_user}")
            repo_name = current_user.repo_name
            repo = await get_repo(github_user,repo_name=repo_name)
            logger.info(f"Github user: {github_user}")
            repo_readme_content = await  get_repo_readme_bulk(repo=repo,user_name=github_user.login,repo_name = current_user.repo_name,uploads=uploads)
            file_structure["README.md"]=repo_readme_content
            await batch_upload_files(repo=repo,file_structure=file_structure)
            # await asyncio.sleep(133)
            
            # await websocket.send_text("Upload Finished !!")
            await websocket.send_json(automatic_websocket_messages[4])

            logger.info("Upload Finished !!")
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")