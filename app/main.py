from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}