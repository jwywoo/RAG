from pydantic import BaseModel

class DatingGenRequestDto(BaseModel):
    title : str
    description : str
    dateTime : str
    activityDescription : str