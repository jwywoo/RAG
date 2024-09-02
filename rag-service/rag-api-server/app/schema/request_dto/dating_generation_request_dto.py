from pydantic import BaseModel

class DatingGenRequestDto(BaseModel):
    query : str