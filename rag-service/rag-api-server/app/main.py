from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "this is message and root"}