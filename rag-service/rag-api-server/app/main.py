from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .routers import dating_generation_router

import os

# Config
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Server Init
app = FastAPI()

# Exception


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Please try again later."},
    )

# Router
app.include_router(dating_generation_router.router)


@app.get("/")
def root():
    return {"message": "this is message and root"}
