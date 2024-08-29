from ..schema.response_dto.dating_generation_response_dto import DatingGenResponseDto

def dating_generation(request):
    generated_dating_response_dto = DatingGenResponseDto(dating=request.query)
    return generated_dating_response_dto