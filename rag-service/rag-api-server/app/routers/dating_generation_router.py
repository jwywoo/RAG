from fastapi import APIRouter

from ..schema.request_dto.dating_generation_request_dto import DatingGenRequestDto
from ..schema.response_dto.dating_generation_response_dto import DatingGenResponseDto

from ..crud.dating_crud import dating_generation

router = APIRouter()

@router.post("/dating/generate", response_model=DatingGenResponseDto)
def dating_generation_router(request: DatingGenRequestDto):
    return dating_generation(request)