from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import users,auth,post,upload
from .config import templates

# Add Jinja2 environment to FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/",response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(upload.router)
