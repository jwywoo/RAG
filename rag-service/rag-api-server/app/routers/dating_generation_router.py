from fastapi import APIRouter

router = APIRouter()

@router.post("/dating/generate")
def create_dating_generation():
    return {"message":"Dating!"}
