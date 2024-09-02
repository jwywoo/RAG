from fastapi import FastAPI
from dotenv import load_dotenv

from .routers import dating_generation_router

import os

# Config
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Server Init
app = FastAPI()

# Router 
app.include_router(dating_generation_router.router)

@app.get("/")
def root():
    return {"message": "this is message and root"}