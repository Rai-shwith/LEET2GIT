from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import users,auth,post,upload

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(upload.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")