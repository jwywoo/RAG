import json
from ...schema.response_dto.dating_generation_response_dto import DatingGenResponseDto


def get_dto(result):
    activities_list = json.loads(result)
    dating_generation_responses = []
    for activity in activities_list:
        response_dto = DatingGenResponseDto(
            activityTitle=activity['activityTitle'],
            activityLocation=activity['activityLoc'],
            timeTotal=activity['timeTotal'],
            activityDescription=activity['activityDescription'],
            activityImage=activity['activityImage']
        )
        dating_generation_responses.append(
            response_dto
        )
    return dating_generation_responses
