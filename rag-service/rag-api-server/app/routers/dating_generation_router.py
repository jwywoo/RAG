from fastapi import APIRouter

from ..schema.request_dto.dating_generation_request_dto import DatingGenRequestDto
from ..schema.response_dto.dating_generation_response_dto import DatingGenResponseDto

router = APIRouter()

@router.post("/dating/generate")
def create_dating_generation(request: DatingGenRequestDto):
    return {"message":"Dating!"}
