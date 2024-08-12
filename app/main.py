from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import users

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(users.router)