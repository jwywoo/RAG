from pydantic import BaseModel


class DatingGenResponseDto(BaseModel):
    activityTitle: str
    activityLocation: str
    timeTotal: str
    activityDescription: str
    activityImage: str
