from fastapi import FastAPI

from .routers import dating_generation_router

# Server Init
app = FastAPI()

# Router 
app.include_router(dating_generation_router.router)

@app.get("/")
def root():
    return {"message": "this is message and root"}